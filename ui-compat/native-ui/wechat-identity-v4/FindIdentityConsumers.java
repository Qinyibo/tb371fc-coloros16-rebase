import java.io.*;
import java.util.*;
import java.util.zip.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.dexbacked.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;
import com.android.tools.smali.baksmali.*;

public class FindIdentityConsumers {
 public static void main(String[] args) throws Exception {
  Set<String> needles = Set.of("Lenovo TB-9707F", "ro.build.characteristics", "ro.product.cpuinfo", "ro.soc.model", "Not support pad", "LoginAsPad", "/cgi-bin/micromsg-bin/checkloginaspad", "doCgi callback loginAsPad:");
  try (ZipFile z = new ZipFile(args[0])) {
   for (ZipEntry entry : Collections.list(z.entries())) {
    if (!entry.getName().matches("classes[0-9]*\\.dex")) continue;
    DexBackedDexFile dex = DexBackedDexFile.fromInputStream(Opcodes.getDefault(), new BufferedInputStream(z.getInputStream(entry)));
    Set<String> selected = new HashSet<>(List.of("Llp/e0;", "Lcp/w0;", "Lcom/tencent/mm/plugin/account/ui/LoginSelectUI$$a;", "Lcom/tencent/mm/ui/ok$$b;", "Lcom/tencent/mm/plugin/account/ui/LoginSelectUI;"));
    for (ClassDef c : dex.getClasses()) for (Method m : c.getMethods()) {
     if (m.getImplementation() == null) continue;
     for (Instruction i : m.getImplementation().getInstructions()) {
      if (i instanceof ReferenceInstruction call && call.getReference() instanceof MethodReference mr && ((mr.getDefiningClass().equals("Ll41/j1;") && mr.getName().equals("a")) || (mr.getDefiningClass().equals("Ll41/h1;") && mr.getName().equals("<init>")))) {
       System.out.println(entry.getName()+" "+c.getType()+"->"+m.getName()+" CALL CHECK_LOGIN_AS_PAD"); selected.add(c.getType());
      }
      if (i instanceof ReferenceInstruction ri && ri.getReference() instanceof StringReference sr && needles.contains(sr.getString())) {
       System.out.println(entry.getName()+" "+c.getType()+"->"+m.getName()+m.getParameterTypes()+m.getReturnType()+" STRING "+sr.getString());
       selected.add(c.getType());
      }
     }
    }
    BaksmaliOptions options = new BaksmaliOptions(); options.debugInfo = false;
    if (!Baksmali.disassembleDexFile(dex, new File(args[0]).getParentFile().toPath().resolve("native-source").toFile(), 1, options, new ArrayList<>(selected))) throw new IOException("Disassembly failed");
   }
  }
 }
}
