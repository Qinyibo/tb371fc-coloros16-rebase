import java.nio.file.*;
import java.util.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.builder.*;
import com.android.tools.smali.dexlib2.builder.instruction.*;
import com.android.tools.smali.dexlib2.dexbacked.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.iface.instruction.*;
import com.android.tools.smali.dexlib2.iface.instruction.formats.Instruction22b;
import com.android.tools.smali.dexlib2.iface.instruction.formats.Instruction11n;
import com.android.tools.smali.dexlib2.iface.reference.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;
public final class OptionalVirtualRadioPatch {
 public static void main(String[] a)throws Exception{
  var dex=new DexBackedDexFile(Opcodes.forApi(36),Files.readAllBytes(Path.of(a[0])));
  var types=new ArrayList<ClassDef>();int changes=0;
  for(var c:dex.getClasses()){
   var methods=new ArrayList<Method>();boolean changed=false;
   for(var m:c.getMethods()){
    com.android.tools.smali.dexlib2.iface.MethodImplementation body=m.getImplementation();
    if(c.getType().equals("Lcom/oplus/internal/telephony/OplusRilImpl;")&&(m.getName().equals("setVirtualServiceProxy")||m.getName().equals("setVirtualRadio"))){
     var b=new MutableMethodImplementation(body);int count=0;
     if(b.getRegisterCount()!=(m.getName().equals("setVirtualRadio")?7:8))throw new IllegalStateException("Unexpected radio locals");
     for(int i=1;i<b.getInstructions().size();i++){
      var ins=b.getInstructions().get(i);
      if(ins instanceof ReferenceInstruction ri&&ri.getReference() instanceof MethodReference mr&&mr.getDefiningClass().equals("Landroid/hardware/radio/V1_5/IRadio;")&&mr.getName().equals("getService")&&mr.getParameterTypes().equals(List.of("Ljava/lang/String;","Z"))){
       var previous=b.getInstructions().get(i-1);
       if(m.getName().equals("setVirtualServiceProxy")){
        if(previous.getOpcode()!=Opcode.XOR_INT_LIT8||!(previous instanceof Instruction22b x)||x.getRegisterA()!=1||x.getRegisterB()!=1||x.getNarrowLiteral()!=1)throw new IllegalStateException("Unexpected proxy retry argument");
       }else{
        if(previous.getOpcode()!=Opcode.CONST_4||!(previous instanceof Instruction11n x)||x.getRegisterA()!=1||x.getNarrowLiteral()!=1)throw new IllegalStateException("Unexpected direct retry argument");
       }
       // Optional radio discovery must return unavailability through the native
       // catch/fallback path rather than block phone startup waiting for absent HALs.
       // The existing connection, callbacks, and all real service results remain.
       b.replaceInstruction(i-1,new BuilderInstruction11n(Opcode.CONST_4,1,0));count++;
      }
     }
     if(count!=1)throw new IllegalStateException("Expected one virtual HIDL service lookup");
     body=b;changed=true;changes++;
    }
    methods.add(new ImmutableMethod(c.getType(),m.getName(),m.getParameters(),m.getReturnType(),m.getAccessFlags(),m.getAnnotations(),m.getHiddenApiRestrictions(),body));
   }
   types.add(changed?new ImmutableClassDef(c.getType(),c.getAccessFlags(),c.getSuperclass(),c.getInterfaces(),c.getSourceFile(),c.getAnnotations(),c.getFields(),methods):c);
  }
  if(changes!=2)throw new IllegalStateException("Expected both native virtual radio lookup methods");
  DexPool.writeTo(a[1],new ImmutableDexFile(dex.getOpcodes(),types));
  System.out.println("OPTIONAL_VIRTUAL_RADIO_NONWAITING_DISCOVERY_CHANGED_TWO_METHODS");
 }
}
