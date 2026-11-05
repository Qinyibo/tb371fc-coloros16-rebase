import java.io.File;
import java.nio.file.Files;
import java.nio.file.Path;
import java.util.regex.Pattern;
import com.android.tools.smali.dexlib2.DexFileFactory;
import com.android.tools.smali.dexlib2.Opcodes;
import com.android.tools.smali.dexlib2.iface.instruction.ReferenceInstruction;
import com.android.tools.smali.dexlib2.iface.reference.MethodReference;
import com.android.tools.smali.baksmali.BaksmaliOptions;
import com.android.tools.smali.baksmali.Adaptors.ClassDefinition;
import com.android.tools.smali.baksmali.formatter.BaksmaliWriter;

class ExtractCameraClientContext {
    public static void main(String[] args) throws Exception {
        var match = Pattern.compile(args[2]);
        var dex = DexFileFactory.loadDexContainer(new File(args[0]), Opcodes.forApi(36));
        var options = new BaksmaliOptions();
        options.apiLevel = 36;
        for (var entry : dex.getDexEntryNames()) {
            for (var type : dex.getEntry(entry).getDexFile().getClasses()) {
                if (!match.matcher(type.getType()).matches() && (args.length < 5 || !calls(type, args[3], args[4]))) {
                    continue;
                }
                var path = Path.of(args[1], type.getType().substring(1, type.getType().length() - 1) + ".smali");
                Files.createDirectories(path.getParent());
                try (var writer = new BaksmaliWriter(Files.newBufferedWriter(path))) {
                    new ClassDefinition(options, type).writeTo(writer);
                }
            }
        }
    }

    private static boolean calls(com.android.tools.smali.dexlib2.iface.ClassDef type, String owner, String name) {
        for (var method : type.getMethods()) {
            if (method.getImplementation() == null) {
                continue;
            }
            for (var instruction : method.getImplementation().getInstructions()) {
                if (instruction instanceof ReferenceInstruction ref && ref.getReference() instanceof MethodReference target
                    && target.getDefiningClass().equals(owner) && target.getName().equals(name)) {
                    System.out.println(type.getType() + " " + method.getName());
                    return true;
                }
            }
        }
        return false;
    }
}
