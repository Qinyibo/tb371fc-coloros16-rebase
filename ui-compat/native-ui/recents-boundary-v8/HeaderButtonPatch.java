import java.nio.file.*;
import java.util.*;
import com.android.tools.smali.dexlib2.*;
import com.android.tools.smali.dexlib2.builder.*;
import com.android.tools.smali.dexlib2.builder.instruction.*;
import com.android.tools.smali.dexlib2.dexbacked.*;
import com.android.tools.smali.dexlib2.iface.*;
import com.android.tools.smali.dexlib2.immutable.*;
import com.android.tools.smali.dexlib2.immutable.reference.*;
import com.android.tools.smali.dexlib2.writer.pool.DexPool;
public final class HeaderButtonPatch {
 static final String HEADER="Lcom/oplus/quickstep/views/OplusTaskHeaderView;";
 public static void main(String[] args)throws Exception{
  var dex=new DexBackedDexFile(Opcodes.forApi(36),Files.readAllBytes(Path.of(args[0])));
  var classes=new ArrayList<ClassDef>();int changes=0;
  for(var type:dex.getClasses()){
   var methods=new ArrayList<Method>();boolean changed=false;
   for(var m:type.getMethods()){
    com.android.tools.smali.dexlib2.iface.MethodImplementation body=m.getImplementation();
    if(type.getType().equals(HEADER)&&m.getName().equals("showSplitWindowIcon")){
     if(!m.getReturnType().equals("V")||m.getParameterTypes().size()!=6)throw new IllegalStateException("Unexpected header entry");
     var b=new MutableMethodImplementation(body);int self=b.getRegisterCount()-7;
     if(self<1)throw new IllegalStateException("Insufficient local registers");
     var original=b.newLabelForIndex(0);
     b.addInstruction(0,new BuilderInstruction35c(Opcode.INVOKE_STATIC,0,0,0,0,0,0,new ImmutableMethodReference("Lcom/oplus/quickstep/common/settingsvalue/CommonSettingsValueProxy;","isStackLayout",List.of(),"Z")));
     b.addInstruction(1,new BuilderInstruction11x(Opcode.MOVE_RESULT,0));
     b.addInstruction(2,new BuilderInstruction21t(Opcode.IF_EQZ,0,original));
     b.addInstruction(3,new BuilderInstruction3rc(Opcode.INVOKE_VIRTUAL_RANGE,self,1,new ImmutableMethodReference(HEADER,"getSplitWindowBtn",List.of(),"Landroid/widget/ImageButton;")));
     b.addInstruction(4,new BuilderInstruction11x(Opcode.MOVE_RESULT_OBJECT,0));
     b.addInstruction(5,new BuilderInstruction21s(Opcode.CONST_16,self+1,8));
     b.addInstruction(6,new BuilderInstruction35c(Opcode.INVOKE_VIRTUAL,2,0,self+1,0,0,0,new ImmutableMethodReference("Landroid/view/View;","setVisibility",List.of("I"),"V")));
     b.addInstruction(7,new BuilderInstruction10x(Opcode.RETURN_VOID));
     body=b;changed=true;changes++;
    }
    methods.add(new ImmutableMethod(type.getType(),m.getName(),m.getParameters(),m.getReturnType(),m.getAccessFlags(),m.getAnnotations(),m.getHiddenApiRestrictions(),body));
   }
   classes.add(changed?new ImmutableClassDef(type.getType(),type.getAccessFlags(),type.getSuperclass(),type.getInterfaces(),type.getSourceFile(),type.getAnnotations(),type.getFields(),methods):type);
  }
  if(changes>0)DexPool.writeTo(args[1],new ImmutableDexFile(dex.getOpcodes(),classes));
  System.out.println("CHANGES "+changes);
 }
}
