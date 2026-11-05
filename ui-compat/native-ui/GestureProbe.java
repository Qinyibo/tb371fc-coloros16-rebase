import android.os.SystemClock;
import android.os.Looper;
import android.content.Context;
import android.view.InputDevice;
import android.view.InputEvent;
import android.view.MotionEvent;
import java.lang.reflect.Method;

/** One finite held swipe through Android's input dispatcher, without accessibility hooks. */
public final class GestureProbe {
    private static Object manager;
    private static Method inject;
    private static Method setDisplay;
    private static long downTime;

    private static void send(int action, float x, float y) throws Exception {
        MotionEvent.PointerProperties finger=new MotionEvent.PointerProperties();
        finger.id=0;finger.toolType=MotionEvent.TOOL_TYPE_FINGER;
        MotionEvent.PointerCoords coordinates=new MotionEvent.PointerCoords();
        coordinates.x=x;coordinates.y=y;coordinates.pressure=1f;coordinates.size=.01f;
        coordinates.touchMajor=8f;coordinates.touchMinor=8f;
        coordinates.toolMajor=8f;coordinates.toolMinor=8f;
        MotionEvent event = MotionEvent.obtain(downTime,SystemClock.uptimeMillis(),action,1,
                new MotionEvent.PointerProperties[]{finger},new MotionEvent.PointerCoords[]{coordinates},
                0,0,1f,1f,-1,0,InputDevice.SOURCE_TOUCHSCREEN,0);
        setDisplay.invoke(event,0);
        try {
            if (!((Boolean) inject.invoke(manager, event, 2))) throw new IllegalStateException("Input event refused");
        } finally { event.recycle(); }
    }

    public static void main(String[] args) throws Exception {
        try { run(args); }
        catch (Throwable failure) {
            System.err.println("GESTURE_PROBE_FAILED");
            failure.printStackTrace();
            System.exit(2);
        }
        System.exit(0);
    }

    private static void run(String[] args) throws Exception {
        if (args.length != 6) throw new IllegalArgumentException("startX startY endX endY durationMs holdMs");
        float sx=Float.parseFloat(args[0]),sy=Float.parseFloat(args[1]);
        float ex=Float.parseFloat(args[2]),ey=Float.parseFloat(args[3]);
        int duration=Integer.parseInt(args[4]),hold=Integer.parseInt(args[5]);
        if (duration < 100 || duration > 1000 || hold < 0 || hold > 1000) throw new IllegalArgumentException("Finite gesture required");
        Looper.prepare();
        Class<?> activityThread=Class.forName("android.app.ActivityThread");
        Object thread=activityThread.getDeclaredMethod("systemMain").invoke(null);
        Context context=(Context)activityThread.getDeclaredMethod("getSystemContext").invoke(thread);
        manager=context.getSystemService(Context.INPUT_SERVICE);
        inject=manager.getClass().getMethod("injectInputEvent",InputEvent.class,int.class);
        setDisplay=InputEvent.class.getMethod("setDisplayId",int.class);
        downTime=SystemClock.uptimeMillis();
        send(MotionEvent.ACTION_DOWN,sx,sy);
        try {
            long end=downTime+duration;
            while (SystemClock.uptimeMillis()<end) {
                float fraction=Math.min(1f,(SystemClock.uptimeMillis()-downTime)/(float)duration);
                send(MotionEvent.ACTION_MOVE,sx+(ex-sx)*fraction,sy+(ey-sy)*fraction);
                Thread.sleep(16);
            }
            send(MotionEvent.ACTION_MOVE,ex,ey);
            Thread.sleep(hold);
            send(MotionEvent.ACTION_MOVE,ex,ey);
        } finally { send(MotionEvent.ACTION_UP,ex,ey); }
        System.out.println("ONE_HELD_SWIPE_INJECTED duration="+duration+" hold="+hold);
    }
}
