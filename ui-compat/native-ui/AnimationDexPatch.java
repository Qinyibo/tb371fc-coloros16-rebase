import java.nio.file.*;
import java.util.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.builder.*;
import com.android.tools.smali.dexlib2.builder.instruction.*;
import com.android.tools.smali.dexlib2.dexbacked.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.immutable.reference.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;

public final class AnimationDexPatch {
 static int count;
 static final String HELPER="Lorg/tb371fc/animation/LauncherCompat;";
 static ImmutableMethodReference ref(String cls,String name,String ret,String... params){return new ImmutableMethodReference(cls,name,Arrays.asList(params),ret);}
 static Method patch(Method m,String mode) {
  if(m.getImplementation()==null)return m;
  String c=m.getDefiningClass(),name=m.getName();
  var b=new MutableMethodImplementation(m.getImplementation());int changed=0;
  if(mode.equals("settings")&&c.equals("Lcom/oplus/settings/feature/display/DisplaySettingsFragment;")&&name.equals("onCreate")&&m.getParameterTypes().size()==1) {
   int self=b.getRegisterCount()-2;
   for(int i=b.getInstructions().size()-1;i>=0;i--)if(b.getInstructions().get(i).getOpcode()==Opcode.RETURN_VOID){
    b.addInstruction(i,new BuilderInstruction3rc(Opcode.INVOKE_STATIC_RANGE,self,1,ref("Lorg/tb371fc/animation/AnimationSettings;","attach","V","Ljava/lang/Object;")));changed++;
   }
  }
  if(mode.equals("launcher")&&c.endsWith("/OplusStackRecentsConfig;")&&name.equals("isAnimLevelSupportedStack")) {
   b=new MutableMethodImplementation(1);
   b.addInstruction(new BuilderInstruction35c(Opcode.INVOKE_STATIC,0,0,0,0,0,0,ref(HELPER,"supportsStack","Z")));
   b.addInstruction(new BuilderInstruction11x(Opcode.MOVE_RESULT,0));b.addInstruction(new BuilderInstruction11x(Opcode.RETURN,0));changed++;
  } else if(mode.equals("launcher")) {
   // Tablet identity alone implies grid cards in the donor. Stack cards must
   // retain their full task size and neutral box translation in both axes.
   if(c.equals("Lcom/android/quickstep/views/OplusTaskViewImpl;")&&name.equals("updateTaskSize")){
    for(int i=0;i<b.getInstructions().size()-1;i++){
     var ins=b.getInstructions().get(i);
     if(ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof MethodReference mr&&mr.getDefiningClass().equals("Lcom/android/launcher/layoutparam/ConfigParam;")&&mr.getName().equals("isTablet")){
      var result=b.getInstructions().get(i+1);
      if(result.getOpcode()!=Opcode.MOVE_RESULT)throw new IllegalStateException("task size tablet result");
      int tablet=((OneRegisterInstruction)result).getRegisterA();
      // v4 is initialized by the immediately following original instruction.
      if(b.getInstructions().get(i+2).getOpcode()!=Opcode.CONST_4||((OneRegisterInstruction)b.getInstructions().get(i+2)).getRegisterA()!=4)throw new IllegalStateException("task size scratch register");
      var resume=b.newLabelForIndex(i+2);
      b.addInstruction(i+2,new BuilderInstruction35c(Opcode.INVOKE_STATIC,0,0,0,0,0,0,ref("Lcom/oplus/quickstep/common/settingsvalue/CommonSettingsValueProxy;","isStackLayout","Z")));
      b.addInstruction(i+3,new BuilderInstruction11x(Opcode.MOVE_RESULT,4));
      b.addInstruction(i+4,new BuilderInstruction21t(Opcode.IF_EQZ,4,resume));
      b.addInstruction(i+5,new BuilderInstruction11n(Opcode.CONST_4,tablet,0));changed++;break;
     }
    }
   }
   if(c.equals("Lcom/android/quickstep/views/TaskView;")&&name.equals("isGridTask")){
    var resume=b.newLabelForIndex(0);
    b.addInstruction(0,new BuilderInstruction35c(Opcode.INVOKE_STATIC,0,0,0,0,0,0,ref("Lcom/oplus/quickstep/common/settingsvalue/CommonSettingsValueProxy;","isStackLayout","Z")));
    b.addInstruction(1,new BuilderInstruction11x(Opcode.MOVE_RESULT,0));
    b.addInstruction(2,new BuilderInstruction21t(Opcode.IF_EQZ,0,resume));
    b.addInstruction(3,new BuilderInstruction11n(Opcode.CONST_4,0,0));
    b.addInstruction(4,new BuilderInstruction11x(Opcode.RETURN,0));changed++;
   }
   if(c.equals("Lcom/android/quickstep/touch/SwipeToRecentMotionPauseDetector;")&&name.equals("addPosition")&&m.getParameterTypes().size()==2){
    int self=b.getRegisterCount()-3,event=self+1;
    // The vendor method reuses p1 for Float before returning: consume the
    // MotionEvent at entry, before its original register type is overwritten.
    b.addInstruction(0,new BuilderInstruction22c(Opcode.IGET,0,self,new ImmutableFieldReference(c,"mScreenHeight","I")));
    b.addInstruction(1,new BuilderInstruction35c(Opcode.INVOKE_VIRTUAL,3,self,event,0,0,0,ref("Lcom/android/quickstep/util/MotionPauseDetector;","r94ArmDesktopPause","V","Landroid/view/MotionEvent;","I")));changed++;
   }
   if(c.endsWith("/RecentsLightAnimUtil;")&&name.equals("isLightRecentAnim")){
    for(int i=b.getInstructions().size()-1;i>=0;i--){
     var ins=b.getInstructions().get(i);
     if(ins.getOpcode()==Opcode.RETURN){
      int r=((OneRegisterInstruction)ins).getRegisterA();
      b.addInstruction(i,new BuilderInstruction35c(Opcode.INVOKE_STATIC,1,r,0,0,0,0,ref(HELPER,"lightRecentWithoutStack","Z","Z")));
      b.addInstruction(i+1,new BuilderInstruction11x(Opcode.MOVE_RESULT,r));changed++;
     }
    }
   }
   boolean timings=(c.equals("Lcom/android/quickstep/AbsSwipeUpHandler;")&&Set.of("getTapToNewTaskDuration","handleNormalGestureEnd").contains(name))
     ||(c.equals("Lcom/android/quickstep/TaskViewUtils;")&&Set.of("composeRecentsLaunchAnimator","createRecentsWindowAnimator").contains(name))
     ||(c.endsWith("/SwipeToRecentAnimationHelper;")&&name.equals("goOverviewAnimation"))
     ||(c.endsWith("/AppToOverviewAnimationProvider;")&&name.equals("getRecentsLaunchDuration"))
     ||(c.endsWith("/RecentsLightAnimUtil;")&&name.equals("isDockIconAndClearAllPanelLightAnim"))
     ||(c.endsWith("/OplusRecentsViewImpl;")&&Set.of("onSwipeUpAnimationSuccess","setControlViewInvisibleWithAnimation","setControlViewVisibleWithAnimation").contains(name))
     ||(c.endsWith("/OplusBaseSwipeUpHandler;")&&(name.equals("onWindowAnimationEnd")||name.startsWith("onWindowAnimationStart$lambda$")));
   for(int i=0;i<b.getInstructions().size();i++){
    var ins=b.getInstructions().get(i);if(!(ins instanceof ReferenceInstruction ri)||!(ri.getReference() instanceof MethodReference mr))continue;
    if(c.equals("Lcom/android/launcher/statemanager/OplusUiFactoryInjector;")&&name.equals("createTouchControllers")&&mr.getDefiningClass().equals("Lcom/android/common/util/PlatformLevelUtils;")&&mr.getName().equals("isAnimationLevel")){
     int level=((FiveRegisterInstruction)ins).getRegisterC();
     b.replaceInstruction(i,new BuilderInstruction35c(Opcode.INVOKE_STATIC,1,level,0,0,0,0,ref(HELPER,"lightDesktopController","Z","I")));changed++;
    }
    if(c.equals("Lcom/android/launcher3/anim/light/AppLaunchAnimUtil;")&&Set.of("getLightDragLayerAnim","getLightLauncherContentAnimation","getLightWindowAnimation").contains(name)&&mr.getName().equals("setDuration")&&mr.getParameterTypes().equals(List.of("J"))){
     if(!(ins instanceof FiveRegisterInstruction args))throw new IllegalStateException("Unexpected light transition duration call");
     int duration=args.getRegisterD();
     b.addInstruction(i,new BuilderInstruction3rc(Opcode.INVOKE_STATIC_RANGE,duration,2,ref(HELPER,"lightLaunchDuration","J","J")));
     b.addInstruction(i+1,new BuilderInstruction11x(Opcode.MOVE_RESULT_WIDE,duration));i+=2;changed++;
    }
    if(timings&&mr.getDefiningClass().equals("Lcom/android/common/util/LauncherAnimConfig;")&&mr.getName().equals("isLevelBOrBPlus")){
     b.replaceInstruction(i,new BuilderInstruction35c(Opcode.INVOKE_STATIC,0,0,0,0,0,0,ref(HELPER,"lightRecentsWithoutStack","Z")));changed++;
    }
    if(c.endsWith("/OplusRecentsViewStateControllerImpl;")&&name.equals("setState")&&mr.getDefiningClass().equals("Lcom/android/common/util/AppFeatureUtils;")&&mr.getName().equals("isLightEnterRecentsAnimation")){
     int receiver=((FiveRegisterInstruction)ins).getRegisterC();
     b.replaceInstruction(i,new BuilderInstruction35c(Opcode.INVOKE_STATIC,1,receiver,0,0,0,0,ref(HELPER,"lightEnterRecentsWithoutStack","Z","Lcom/android/common/util/AppFeatureUtils;")));changed++;
    }
    if(c.endsWith("/OplusTaskViewImpl;")&&name.equals("_init_$lambda$7")&&mr.getDefiningClass().equals("Lcom/android/common/util/LauncherAnimConfig;")&&mr.getName().equals("isAdaptiveLowAnimation")){
     b.replaceInstruction(i,new BuilderInstruction35c(Opcode.INVOKE_STATIC,0,0,0,0,0,0,ref(HELPER,"adaptiveLowWithoutStack","Z")));changed++;
    }
   }
   if(c.equals("Lcom/android/quickstep/AbsSwipeUpHandler;")&&name.equals("handleNormalGestureEnd")){
    for(int i=b.getInstructions().size()-1;i>=0;i--){
     var ins=b.getInstructions().get(i);
     if(ins instanceof WideLiteralInstruction lit&&lit.getWideLiteral()==700&&ins instanceof OneRegisterInstruction reg){
      int r=reg.getRegisterA();
      b.addInstruction(i+1,new BuilderInstruction3rc(Opcode.INVOKE_STATIC_RANGE,r,2,ref(HELPER,"stackTransitionDuration","J","J")));
      b.addInstruction(i+2,new BuilderInstruction11x(Opcode.MOVE_RESULT_WIDE,r));changed++;
     }
    }
   }
   if(c.equals("Lcom/android/quickstep/util/MotionPauseDetector;")&&Set.of("addPosition","checkMotionPaused").contains(name)){
    for(int i=b.getInstructions().size()-1;i>=0;i--){
     var ins=b.getInstructions().get(i);
     if(ins instanceof WideLiteralInstruction lit&&(lit.getWideLiteral()==300||lit.getWideLiteral()==400)&&ins instanceof OneRegisterInstruction reg){
      int r=reg.getRegisterA();
      b.addInstruction(i+1,new BuilderInstruction3rc(Opcode.INVOKE_STATIC_RANGE,r,2,ref(HELPER,"recentsPauseTimeout","J","J")));
      b.addInstruction(i+2,new BuilderInstruction11x(Opcode.MOVE_RESULT_WIDE,r));changed++;
     }
    }
   }
  }
  // Keep the native grid/database mapping. TB's 16:10 viewport can overflow
  // the donor's square cells, so retain the native viewport-fit algorithm
  // for tablets as well. Fold/two-panel/orientation and resource guards stay.
  if(mode.equals("launcher")&&c.equals("Lcom/android/launcher/layoutparam/CellLayoutParam;")&&Set.of("applyPhoneViewportCellHeightCapIfNeeded","shouldApplyPhoneViewportCellHeightCap").contains(name)){
   for(int i=0;i<b.getInstructions().size()-2;i++){
    var ins=b.getInstructions().get(i);
    if(ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof MethodReference mr&&mr.getDefiningClass().equals("Lcom/android/common/util/AppFeatureUtils;")&&mr.getName().equals("isTablet")){
     if(b.getInstructions().get(i+1).getOpcode()!=Opcode.MOVE_RESULT)throw new IllegalStateException("viewport result shape");
     int reg=((OneRegisterInstruction)b.getInstructions().get(i+1)).getRegisterA();boolean found=false;
     for(int k=i+2;k<Math.min(i+5,b.getInstructions().size());k++)if(b.getInstructions().get(k).getOpcode()==Opcode.IF_NEZ&&((OneRegisterInstruction)b.getInstructions().get(k)).getRegisterA()==reg){
      b.replaceInstruction(k,new BuilderInstruction10x(Opcode.NOP));changed++;found=true;break;
     }
     if(!found)throw new IllegalStateException("viewport exemption branch shape");
    }
   }
   if(name.equals("applyPhoneViewportCellHeightCapIfNeeded"))for(int i=0;i<b.getInstructions().size()-2;i++){
    var ins=b.getInstructions().get(i);
    if(ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof MethodReference mr&&mr.getDefiningClass().equals("Lcom/android/launcher/layoutparam/ConfigParam;")&&mr.getName().equals("getRealNavBarHeight")){
     var add=b.getInstructions().get(i+2);
     if(b.getInstructions().get(i+1).getOpcode()!=Opcode.MOVE_RESULT||add.getOpcode()!=Opcode.ADD_INT_2ADDR)throw new IllegalStateException("viewport navigation budget shape: "+add.getOpcode());
     var regs=(TwoRegisterInstruction)add;
     // TB's availableHeight already describes the actual usable tablet
     // viewport. Adding a nominal navigation-bar height back overstates it.
     b.replaceInstruction(i+2,new BuilderInstruction12x(Opcode.MOVE,regs.getRegisterA(),regs.getRegisterB()));changed++;break;
    }
   }
  }
  // Both modes use the high-quality wallpaper backdrop; tier 3 selects that path.
  // Keep all other AssistantScreen animation, card and material gates intact.
  // The .600 tablet product disables these native UI capabilities by policy.
  // Keep tablet identity and all hardware contracts unchanged.
  if(mode.equals("launcher")&&c.equals("Lcom/oplus/quickstep/layout/stack/OplusStackRecentsConfig;")&&name.equals("isStackSupported")){
   for(int i=0;i<b.getInstructions().size()-1;i++){
    var ins=b.getInstructions().get(i);
    if(ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof MethodReference mr&&mr.getName().equals("isTablet")){
     int reg=((OneRegisterInstruction)b.getInstructions().get(i+1)).getRegisterA();
     b.replaceInstruction(i,new BuilderInstruction11n(Opcode.CONST_4,reg,0));
     b.replaceInstruction(i+1,new BuilderInstruction10x(Opcode.NOP));changed++;
    }
   }
  }
  if(mode.equals("launcher")&&c.equals("Lcom/oplus/quickstep/layout/grid/OplusGridRecentsConfig;")&&name.equals("isEnable")){
   for(int i=b.getInstructions().size()-1;i>=0;i--)if(b.getInstructions().get(i).getOpcode()==Opcode.RETURN){
    int reg=((OneRegisterInstruction)b.getInstructions().get(i)).getRegisterA();
    b.addInstruction(i,new BuilderInstruction35c(Opcode.INVOKE_STATIC,1,reg,0,0,0,0,ref(HELPER,"useGridRecents","Z","Z")));
    b.addInstruction(i+1,new BuilderInstruction11x(Opcode.MOVE_RESULT,reg));changed++;
   }
  }
  if(mode.equals("launcher")&&c.equals("Lcom/oplus/quickstep/memory/MemoryInfoManager;")){
   if(name.equals("judgeWhetherAllowMemoDisplay"))for(int i=0;i<b.getInstructions().size();i++){
    var ins=b.getInstructions().get(i);
    if(ins instanceof NarrowLiteralInstruction lit&&lit.getNarrowLiteral()==34){
     int reg=((OneRegisterInstruction)ins).getRegisterA();b.replaceInstruction(i,new BuilderInstruction21s(Opcode.CONST_16,reg,36));changed++;
    }
   }
   if(name.equals("updateMemoDisplaySwitch"))for(int i=0;i<b.getInstructions().size();i++){
    var ins=b.getInstructions().get(i);
    if(ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof MethodReference mr&&mr.getDefiningClass().equals("Landroid/provider/Settings$Secure;")&&mr.getName().equals("getInt")){
     int reg=((FiveRegisterInstruction)ins).getRegisterE();
     if(b.getInstructions().get(i+1).getOpcode()!=Opcode.MOVE_RESULT)throw new IllegalStateException("memory result shape");
     b.addInstruction(i,new BuilderInstruction11n(Opcode.CONST_4,reg,1));
     b.addInstruction(i+3,new BuilderInstruction11n(Opcode.CONST_4,reg,0));i+=3;changed++;
    }
   }
  }
  if(mode.equals("launcher")&&c.equals("Lcom/oplus/effectengine/OplusEffect;")&&name.equals("initEGL")){
   for(int i=0;i<b.getInstructions().size();i++){
    var ins=b.getInstructions().get(i);
    if(ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof MethodReference mr&&mr.getDefiningClass().equals("Landroid/media/ImageReader;")&&mr.getName().equals("setOnImageAvailableListener")){
     int reg=((FiveRegisterInstruction)ins).getRegisterE();
     b.addInstruction(i,new BuilderInstruction35c(Opcode.INVOKE_STATIC,1,reg,0,0,0,0,ref(HELPER,"imageCallbackHandler","Landroid/os/Handler;","Landroid/os/Handler;")));
     b.addInstruction(i+1,new BuilderInstruction11x(Opcode.MOVE_RESULT_OBJECT,reg));i+=2;changed++;
    }
   }
  }
  if(mode.equals("assistant")&&c.equals("LNo/u;")&&name.equals("f")&&m.getParameterTypes().equals(List.of("Landroid/view/View;"))){
   for(int i=0;i<b.getInstructions().size()-1;i++){
    var ins=b.getInstructions().get(i);
    if(ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof MethodReference mr&&mr.getDefiningClass().equals("Lxk/d0;")&&mr.getName().equals("c")){
     int reg=((OneRegisterInstruction)b.getInstructions().get(i+1)).getRegisterA();
     // This local value selects backdrop quality; no global GPU capability spoof.
     b.replaceInstruction(i,new BuilderInstruction11n(Opcode.CONST_4,reg,3));
     b.replaceInstruction(i+1,new BuilderInstruction10x(Opcode.NOP));changed++;
    }
   }
  }
  if(changed==0)return m;
  count+=changed;if(changed>0)System.out.println("EDIT "+c+"->"+name+" changes="+changed);
  return new ImmutableMethod(c,name,m.getParameters(),m.getReturnType(),m.getAccessFlags(),m.getAnnotations(),m.getHiddenApiRestrictions(),b);
 }
 public static void main(String[] args)throws Exception{
  var dex=new DexBackedDexFile(Opcodes.forApi(36),Files.readAllBytes(Path.of(args[0])));var classes=new ArrayList<ClassDef>();var moved=new ArrayList<ClassDef>();
  for(var c:dex.getClasses()){
   int before=count;
   var methods=new ArrayList<Method>();for(var m:c.getMethods())methods.add(patch(m,args[2]));
   if(args[2].equals("launcher")&&c.getType().equals("Lcom/android/quickstep/util/MotionPauseDetector;")){
    var impl=new MutableMethodImplementation(4);
    impl.addInstruction(new BuilderInstruction22c(Opcode.IGET_OBJECT,0,1,new ImmutableFieldReference(c.getType(),"mForcePauseTimeout","Lcom/android/launcher3/Alarm;")));
    impl.addInstruction(new BuilderInstruction35c(Opcode.INVOKE_STATIC,3,0,2,3,0,0,ref(HELPER,"desktopPause","V","Lcom/android/launcher3/Alarm;","Landroid/view/MotionEvent;","I")));
    impl.addInstruction(new BuilderInstruction10x(Opcode.RETURN_VOID));
    methods.add(new ImmutableMethod(c.getType(),"r94ArmDesktopPause",List.of(new ImmutableMethodParameter("Landroid/view/MotionEvent;",Set.of(),null),new ImmutableMethodParameter("I",Set.of(),null)),"V",1,Set.of(),Set.of(),impl));
    count++;System.out.println("EDIT "+c.getType()+"->r94ArmDesktopPause changes=1");
   }
   var next=new ImmutableClassDef(c.getType(),c.getAccessFlags(),c.getSuperclass(),c.getInterfaces(),c.getSourceFile(),c.getAnnotations(),c.getFields(),methods);
   // Vendor dex files are at the 65536 method-reference limit. Move changed
   // classes into a new dex instead of overflowing or deleting vendor code.
   if(count>before&&!args[2].equals("assistant"))moved.add(next);else classes.add(next);
  }
  if(count>0)DexPool.writeTo(args[1],new ImmutableDexFile(dex.getOpcodes(),classes));
  if(!moved.isEmpty())DexPool.writeTo(args[1]+".moved",new ImmutableDexFile(dex.getOpcodes(),moved));
  System.out.println("PATCHED "+count);
 }
}
