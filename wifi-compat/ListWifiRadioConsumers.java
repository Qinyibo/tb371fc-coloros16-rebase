import java.io.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.reference.*;
public final class ListWifiRadioConsumers {
 public static void main(String[] args) throws Exception {
  var container=DexFileFactory.loadDexContainer(new File(args[0]),Opcodes.forApi(36));
  for(var entry:container.getDexEntryNames()) for(var c:container.getEntry(entry).getDexFile().getClasses()) for(var m:c.getMethods()) {
   if(m.getImplementation()==null)continue;int reads=0;
   for(var i:m.getImplementation().getInstructions())if(i instanceof ReferenceInstruction r && r.getReference() instanceof FieldReference f && f.getDefiningClass().equals("Lcom/android/server/wifi/WifiLinkLayerStats;") && f.getName().equals("radioStats") && i.getOpcode()==Opcode.IGET_OBJECT)reads++;
   if(reads>0)System.out.println(c.getType()+"->"+m.getName()+m.getParameterTypes()+" reads="+reads);
  }
 }
}
