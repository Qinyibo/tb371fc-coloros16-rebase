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
import com.android.tools.smali.dexlib2.writer.pool.DexPool;

/** Preserve aggregate channel statistics when old HIDL does not expose per-radio statistics. */
public final class WifiOptionalRadioStatsPatch {
    private static final String OWNER = "Lcom/android/server/wifi/WifiChannelUtilization;";
    public static void main(String[] args) throws Exception {
        var dex = new DexBackedDexFile(Opcodes.forApi(36), Files.readAllBytes(Path.of(args[0])));
        var classes = new ArrayList<ClassDef>(); int edits = 0;
        for (var c : dex.getClasses()) {
            if (!c.getType().equals(OWNER)) { classes.add(c); continue; }
            var methods = new ArrayList<Method>();
            for (var m : c.getMethods()) {
                if (!m.getName().equals("refreshChannelStatsAndChannelUtilization")) { methods.add(m); continue; }
                if (!m.getParameterTypes().equals(List.of("Lcom/android/server/wifi/WifiLinkLayerStats;", "I")) || !m.getReturnType().equals("V")) throw new IllegalStateException("Unexpected method signature");
                var b = new MutableMethodImplementation(m.getImplementation());
                int matches = 0;
                for (int i = 1; i < b.getInstructions().size(); i++) {
                    var ins = b.getInstructions().get(i); var prev = b.getInstructions().get(i-1);
                    if (ins.getOpcode() != Opcode.ARRAY_LENGTH || !(prev instanceof ReferenceInstruction ref) || !(ref.getReference() instanceof FieldReference field) || !field.getDefiningClass().equals("Lcom/android/server/wifi/WifiLinkLayerStats;") || !field.getName().equals("radioStats")) continue;
                    var regs = (TwoRegisterInstruction) ins;
                    if (regs.getRegisterA() != 2 || regs.getRegisterB() != 1 || b.getRegisterCount() != 13) throw new IllegalStateException("Unexpected register layout");
                    var hasStats = b.newLabelForIndex(i); var initLoop = b.newLabelForIndex(i+1);
                    b.addInstruction(i, new BuilderInstruction21t(Opcode.IF_NEZ, 1, hasStats));
                    b.addInstruction(i+1, new BuilderInstruction11n(Opcode.CONST_4, 2, 0));
                    b.addInstruction(i+2, new BuilderInstruction10t(Opcode.GOTO, initLoop));
                    matches++; break;
                }
                if (matches != 1) throw new IllegalStateException("Expected one optional radio array use");
                methods.add(new ImmutableMethod(OWNER, m.getName(), m.getParameters(), m.getReturnType(), m.getAccessFlags(), m.getAnnotations(), m.getHiddenApiRestrictions(), b)); edits++;
            }
            classes.add(new ImmutableClassDef(c.getType(), c.getAccessFlags(), c.getSuperclass(), c.getInterfaces(), c.getSourceFile(), c.getAnnotations(), c.getFields(), methods));
        }
        if (edits != 1) throw new IllegalStateException("Expected one method, got " + edits);
        DexPool.writeTo(args[1], new ImmutableDexFile(dex.getOpcodes(), classes));
        System.out.println("OPTIONAL_RADIO_STATS_GUARD_BUILT_AGGREGATE_PATH_PRESERVED");
    }
}
