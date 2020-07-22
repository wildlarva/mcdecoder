Search.setIndex({docnames:["README","dev_coding_style","dev_coding_style_c","dev_coding_style_cpp","dev_coding_style_python","dev_design","dev_docs","dev_guides","dev_modules","guides","index","quickstart","spec_commandline_options","spec_limit","spec_mc_desc","spec_mcdecoder_api","spec_mcdecoder_model","spec_template_var","specifications","user_templates"],envversion:{"sphinx.domains.c":2,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":3,"sphinx.domains.index":1,"sphinx.domains.javascript":2,"sphinx.domains.math":2,"sphinx.domains.python":2,"sphinx.domains.rst":2,"sphinx.domains.std":1,sphinx:56},filenames:["README.rst","dev_coding_style.rst","dev_coding_style_c.rst","dev_coding_style_cpp.rst","dev_coding_style_python.rst","dev_design.rst","dev_docs.rst","dev_guides.rst","dev_modules.rst","guides.rst","index.rst","quickstart.rst","spec_commandline_options.rst","spec_limit.rst","spec_mc_desc.rst","spec_mcdecoder_api.rst","spec_mcdecoder_model.rst","spec_template_var.rst","specifications.rst","user_templates.rst"],objects:{"":{DecodeInstruction:[15,0,1,"c.DecodeInstruction"],DecodeRequest:[15,1,1,"c.DecodeRequest"],DecodeResult:[15,1,1,"c.DecodeResult"],INSTRUCTION_ID_MAX:[15,4,1,"c.INSTRUCTION_ID_MAX"],InstructionId:[15,5,1,"c.InstructionId"]},"mcdecoder.__main__":{main:[8,8,1,""]},"mcdecoder.__version__":{__version__:[8,9,1,""]},"mcdecoder.app":{run_app:[8,8,1,""]},"mcdecoder.checker":{check:[8,8,1,""]},"mcdecoder.common":{bit_length_of_character:[8,8,1,""],convert_to_big_endian:[8,8,1,""],make_mask:[8,8,1,""],make_parent_directories:[8,8,1,""],pad_trailing_zeros:[8,8,1,""],string_length_for_byte:[8,8,1,""],trim_whitespace:[8,8,1,""]},"mcdecoder.core":{AndIdCondition:[8,10,1,""],BitRangeDescription:[8,10,1,""],DecodeContext:[8,10,1,""],DecodeContextVectorized:[8,10,1,""],EqualityIdCondition:[8,10,1,""],EqualityInstructionConditionDescription:[8,10,1,""],FieldIdConditionObject:[8,10,1,""],FieldInstructionConditionObjectDescription:[8,10,1,""],FunctionIdConditionObject:[8,10,1,""],FunctionInstructionConditionObjectDescription:[8,10,1,""],ImmediateIdConditionObject:[8,10,1,""],ImmediateInstructionConditionObjectDescription:[8,10,1,""],InIdCondition:[8,10,1,""],InInstructionConditionDescription:[8,10,1,""],InRangeIdCondition:[8,10,1,""],InRangeInstructionConditionDescription:[8,10,1,""],InstructionConditionDescription:[8,10,1,""],InstructionConditionObjectDescription:[8,10,1,""],InstructionDecodeResult:[8,10,1,""],InstructionDecoder:[8,10,1,""],InstructionDecoderCondition:[8,10,1,""],InstructionDecoderConditionObject:[8,10,1,""],InstructionDescription:[8,10,1,""],InstructionEncodingDescription:[8,10,1,""],InstructionEncodingElementDescription:[8,10,1,""],InstructionFieldDecodeResult:[8,10,1,""],InstructionFieldDecoder:[8,10,1,""],InstructionFieldEncodingDescription:[8,10,1,""],InstructionSubfieldDecoder:[8,10,1,""],LoadError:[8,13,1,""],LogicalInstructionConditionDescription:[8,10,1,""],MachineDecoder:[8,10,1,""],MachineDescription:[8,10,1,""],McDecoder:[8,10,1,""],McDecoderDescription:[8,10,1,""],McDescription:[8,10,1,""],McdDecisionNode:[8,10,1,""],McdDecisionTree:[8,10,1,""],OrIdCondition:[8,10,1,""],calc_instruction_bit_size:[8,8,1,""],create_mcdecoder_model:[8,8,1,""],decode_instruction:[8,8,1,""],find_matched_instructions:[8,8,1,""],find_matched_instructions_vectorized:[8,8,1,""],load_mc_description_model:[8,8,1,""],parse_instruction_encoding:[8,8,1,""]},"mcdecoder.core.AndIdCondition":{conditions:[8,11,1,""],type:[8,12,1,""]},"mcdecoder.core.BitRangeDescription":{end:[8,11,1,""],start:[8,11,1,""]},"mcdecoder.core.DecodeContext":{code16x1:[8,11,1,""],code16x2:[8,11,1,""],code32x1:[8,11,1,""],mcdecoder:[8,11,1,""]},"mcdecoder.core.DecodeContextVectorized":{code16x1_vec:[8,11,1,""],code16x2_vec:[8,11,1,""],code32x1_vec:[8,11,1,""],mcdecoder:[8,11,1,""]},"mcdecoder.core.EqualityIdCondition":{object:[8,11,1,""],operator:[8,11,1,""],subject:[8,11,1,""],type:[8,12,1,""]},"mcdecoder.core.EqualityInstructionConditionDescription":{object:[8,11,1,""],operator:[8,11,1,""],subject:[8,11,1,""]},"mcdecoder.core.FieldIdConditionObject":{element_index:[8,11,1,""],field:[8,11,1,""],type:[8,12,1,""]},"mcdecoder.core.FieldInstructionConditionObjectDescription":{element_index:[8,11,1,""],field:[8,11,1,""]},"mcdecoder.core.FunctionIdConditionObject":{"function":[8,11,1,""],argument:[8,11,1,""],type:[8,12,1,""]},"mcdecoder.core.FunctionInstructionConditionObjectDescription":{"function":[8,11,1,""],argument:[8,11,1,""]},"mcdecoder.core.ImmediateIdConditionObject":{type:[8,12,1,""],value:[8,11,1,""]},"mcdecoder.core.ImmediateInstructionConditionObjectDescription":{value:[8,11,1,""]},"mcdecoder.core.InIdCondition":{subject:[8,11,1,""],type:[8,12,1,""],values:[8,11,1,""]},"mcdecoder.core.InInstructionConditionDescription":{subject:[8,11,1,""],values:[8,11,1,""]},"mcdecoder.core.InRangeIdCondition":{subject:[8,11,1,""],type:[8,12,1,""],value_end:[8,11,1,""],value_start:[8,11,1,""]},"mcdecoder.core.InRangeInstructionConditionDescription":{subject:[8,11,1,""],value_end:[8,11,1,""],value_start:[8,11,1,""]},"mcdecoder.core.InstructionDecodeResult":{decoder:[8,11,1,""],field_results:[8,12,1,""],fields:[8,11,1,""]},"mcdecoder.core.InstructionDecoder":{encoding_element_bit_length:[8,11,1,""],extras:[8,11,1,""],field_decoders:[8,12,1,""],fields:[8,11,1,""],fixed_bit_mask:[8,11,1,""],fixed_bits:[8,11,1,""],fixed_bits_mask:[8,12,1,""],length_of_encoding_elements:[8,11,1,""],match_condition:[8,11,1,""],name:[8,11,1,""],type_bit_length:[8,11,1,""],type_bit_size:[8,12,1,""],unmatch_condition:[8,11,1,""]},"mcdecoder.core.InstructionDecoderCondition":{type:[8,12,1,""]},"mcdecoder.core.InstructionDecoderConditionObject":{type:[8,12,1,""]},"mcdecoder.core.InstructionDescription":{extras:[8,11,1,""],field_extras:[8,11,1,""],format:[8,11,1,""],match_condition:[8,11,1,""],name:[8,11,1,""],unmatch_condition:[8,11,1,""]},"mcdecoder.core.InstructionEncodingDescription":{elements:[8,11,1,""]},"mcdecoder.core.InstructionEncodingElementDescription":{fields:[8,11,1,""]},"mcdecoder.core.InstructionFieldDecodeResult":{decoder:[8,11,1,""],value:[8,11,1,""]},"mcdecoder.core.InstructionFieldDecoder":{extras:[8,11,1,""],name:[8,11,1,""],subfield_decoders:[8,12,1,""],subfields:[8,11,1,""],type_bit_length:[8,11,1,""],type_bit_size:[8,12,1,""]},"mcdecoder.core.InstructionFieldEncodingDescription":{bit_ranges:[8,11,1,""],bits_format:[8,11,1,""],name:[8,11,1,""]},"mcdecoder.core.InstructionSubfieldDecoder":{end_bit_in_field:[8,12,1,""],end_bit_in_instruction:[8,12,1,""],index:[8,11,1,""],lsb_in_field:[8,11,1,""],lsb_in_instruction:[8,11,1,""],mask:[8,11,1,""],msb_in_instruction:[8,11,1,""],start_bit_in_instruction:[8,12,1,""]},"mcdecoder.core.LoadError":{message:[8,11,1,""]},"mcdecoder.core.LogicalInstructionConditionDescription":{conditions:[8,11,1,""],operator:[8,11,1,""]},"mcdecoder.core.MachineDecoder":{byteorder:[8,11,1,""],extras:[8,11,1,""]},"mcdecoder.core.MachineDescription":{byteorder:[8,11,1,""],extras:[8,11,1,""]},"mcdecoder.core.McDecoder":{decision_trees:[8,11,1,""],extras:[8,11,1,""],instruction_decoders:[8,12,1,""],instructions:[8,11,1,""],machine:[8,11,1,""],machine_decoder:[8,12,1,""],namespace:[8,11,1,""],namespace_prefix:[8,11,1,""]},"mcdecoder.core.McDecoderDescription":{namespace:[8,11,1,""],process_instruction_hook:[8,11,1,""]},"mcdecoder.core.McDescription":{decoder:[8,11,1,""],extras:[8,11,1,""],instructions:[8,11,1,""],machine:[8,11,1,""]},"mcdecoder.core.McdDecisionNode":{all_nodes:[8,12,1,""],arbitrary_bit_node:[8,11,1,""],fixed_bit_nodes:[8,11,1,""],index:[8,11,1,""],instructions:[8,11,1,""],mask:[8,11,1,""]},"mcdecoder.core.McdDecisionTree":{encoding_element_bit_length:[8,11,1,""],length_of_encoding_elements:[8,11,1,""],root_node:[8,11,1,""]},"mcdecoder.core.OrIdCondition":{conditions:[8,11,1,""],type:[8,12,1,""]},"mcdecoder.emulator":{emulate:[8,8,1,""]},"mcdecoder.exporter":{"export":[8,8,1,""]},"mcdecoder.generator":{generate:[8,8,1,""]},DecodeRequest:{codes:[15,2,1,"c.DecodeRequest.codes"]},DecodeResult:{instruction:[15,3,1,"c.DecodeResult.instruction"],instruction_id:[15,2,1,"c.DecodeResult.instruction_id"]},InstructionId:{InstructionId_kUnknown:[15,6,1,"c.InstructionId.InstructionId_kUnknown"]},mcdecoder:{__main__:[8,7,0,"-"],__version__:[8,7,0,"-"],app:[8,7,0,"-"],checker:[8,7,0,"-"],common:[8,7,0,"-"],core:[8,7,0,"-"],emulator:[8,7,0,"-"],exporter:[8,7,0,"-"],generator:[8,7,0,"-"]}},objnames:{"0":["c","function","C function"],"1":["c","struct","struct"],"10":["py","class","Python class"],"11":["py","attribute","Python attribute"],"12":["py","method","Python method"],"13":["py","exception","Python exception"],"2":["c","member","C member"],"3":["c","union","union"],"4":["c","var","C variable"],"5":["c","enum","enum"],"6":["c","enumerator","enumerator"],"7":["py","module","Python module"],"8":["py","function","Python function"],"9":["py","data","Python data"]},objtypes:{"0":"c:function","1":"c:struct","10":"py:class","11":"py:attribute","12":"py:method","13":"py:exception","2":"c:member","3":"c:union","4":"c:var","5":"c:enum","6":"c:enumerator","7":"py:module","8":"py:function","9":"py:data"},terms:{"002d4800":12,"00482de9":12,"092d4800":12,"0b0":11,"0b100":11,"0b1011":11,"0b1101":11,"0b1110":11,"0b1111":[11,14],"0th":[8,16],"0x0":11,"0x00":15,"0x04":[0,11],"0x2d":15,"0x4":11,"0x48":15,"0x8d":[0,11],"0xb":11,"0xb0":[0,11],"0xd":11,"0xe":11,"0xe2":[0,11],"0xe9":15,"0xf":14,"15th":14,"1a6":[8,16],"1b1":[8,12,16,17],"1x10":12,"abstract":[8,16],"boolean":8,"break":[11,15],"byte":[8,12,14,16],"case":[11,15],"class":[8,16],"const":[0,11,15,19],"default":[8,11,12],"enum":[14,15],"export":[5,6,11],"final":19,"function":[2,3,5,8,11,14,16,18],"import":14,"int":[8,11,16],"public":7,"return":[5,8,11,15],"short":2,"static":0,"switch":[7,11,15],"true":[8,15],"void":11,"while":8,AND:[8,16],And:19,For:[2,3,9,11],Its:11,One:14,The:[0,2,3,4,7,8,12,13,14,16,19],There:2,These:14,Use:[0,2,3,4,8,11,16,19],Used:5,Uses:[5,8,16],With:[2,3],__main__:[5,6],__version__:[5,6],_encod:[8,16],_instruct:14,_msb:[8,16],about:[5,9,11,17,19],abov:[2,7],access:19,accord:[5,11,12],act:12,activ:7,actual:0,add:[2,3,4,7,9],add_1:[14,19],add_immediate_a1:[0,11],add_instruct:14,added:8,addit:[1,8,11,18,19],additionalproperti:14,adjac:14,after:7,against:[5,8],align:8,all:[5,8,11,14],all_nod:[8,16],allow:19,also:[2,3,4,14],alwai:[8,16],ambigu:2,among:2,analyz:0,andidcondit:[8,16],ani:[8,14,16,17,19],anoth:[8,12,14],anywher:14,api:[2,3,7,10,11,12,18],app:[5,6,11],appli:[7,8,14,16],applic:8,approach:0,appropri:15,apt:7,arbitrari:[8,16],arbitrary_bit_nod:[8,16],arch_typ:[14,19],architectur:19,arg:8,argpars:5,argument:[8,14,16,18],argv:8,arm:[0,14,19],arm_const:19,arm_decodeerror:2,arm_decodeerrors_kok:2,arm_decoderesult:2,arm_kdecodeerrorsmax:2,arm_printinstruct:2,arrai:14,assembl:11,asterisk:14,athril:[0,8,12],attribut:[8,14,16,19],automat:5,back:10,bar:14,base:[2,3,4,5,8,12,14,16],basic:0,becaus:[2,3,4],befor:[11,14],behav:5,behavior:[11,14],below:[0,11,13,14,19],between:[2,3,4,14],big:[8,12,14,16],billion:5,bin:7,binari:[0,8,12],bintrai:7,bit:[8,11,13,14,16],bit_length_of_charact:8,bit_pattern:8,bit_rang:8,bit_siz:8,bitrangedescript:8,bits_format:8,bool:[0,8,11,15],both:5,boundari:[2,3],build:[5,6],bundl:7,bundler:[5,7],byteord:[0,8,11,12,16,19],c11:2,c18:2,c_decod:12,calc_instruction_bit_s:8,calcul:[5,8],call:[8,11,14,16,19],can:[2,3,4,11,14,19],cannot:4,certain:[5,11,12],chang:[7,14],charact:[2,8,12,14],check:[0,5,8,9,19],checker:[5,6],child:[8,16],choic:12,clarifi:[2,3],clean:7,client:[0,9],clock:[14,19],clone:[0,7],code16x1:8,code16x1_vec:8,code16x2:8,code16x2_vec:8,code32x1:8,code32x1_vec:8,code:[0,5,6,8,9,10,12,14,15,16,17],coincid:11,com:[0,7],combin:[8,14,16],comma:14,command:[5,8,10,11,18,19],common:[3,5,6],compil:[11,14,19],comput:13,conan:[5,7],cond:[0,11,14,15,19],condit:[8,11,18],config:14,conflict:4,consid:5,consist:[3,14],constant:[2,3,19],construct:14,contain:[8,19],content:[1,5,6,9,10,11,14,18,19],context:8,convers:8,convert:[5,8],convert_to_big_endian:8,core:[5,6,14,16],correct:2,correspond:[8,12],count:14,cov:[5,7],coverag:[5,7],cpp:5,cpu:0,creat:[5,7,8,9,11],create_mcdecoder_model:8,csv:[8,11,12],cucumb:5,cumbersom:0,current:[8,12],custom:11,data:[0,8,9,12,14,16,17],decid:[8,16],decis:[8,18],decision_tre:[8,16],decod:[0,5,6,8,9,10,12,13,17,18,19],decode_instruct:8,decodecontext:8,decodecontextvector:8,decodeerrors_add:3,decodeerrors_kok:2,decodeinstruct:[0,2,3,11,15],decodeinstruction_add:2,decoderequest:[0,2,3,11,15],decoderequest_add:2,decoderesult:[0,11,15],decoderesult_add:3,def:14,defin:[0,5,8,9,11,12,14,16,17],depend:14,deprec:[5,8,12,16,17],depth:[8,16],descend:[8,16],describ:[8,14],descript:[5,8,9,10,12,17,18],design:[6,10,19],dest:14,detail:[9,11,19],detect:12,dev1:8,dev:7,develop:[4,9,10],diagram:5,dict:[8,16],dictionari:[8,16],did:11,differ:[3,14],directoi:12,directori:[4,7,8,12,14,19],dispatch:5,doc:5,document:[0,5,19],doe:[5,8,14],doesn:2,don:19,doubl:14,doxygen:[2,3],duplic:12,e28db004:11,e92d4800:12,each:[5,8,11,14,16],easili:3,either:3,element:[8,11,14,16,17],element_index:[8,16],els:[11,19],emul:[0,5,6,11],encod:[8,9,13,14,16],encoding_element_bit_length:[8,16],end:[8,14,16],end_bit_in_field:[8,16],end_bit_in_instruct:[8,16],endfor:19,endian:[8,12,13,14],endif:19,entri:8,entrypoint:5,enumer:[3,15],enumeration_typ:2,env:7,environ:[2,4,6],equal:[8,16],equalityidcondit:[8,16],equalityinstructionconditiondescript:8,error:[8,14],etc:[0,2,3,5,8,13,14],even:4,exampl:[2,3,5,9,14,15,19],excel:11,except:[1,8],exclus:14,execut:[8,11],exist:19,exit:[8,12],expect:8,expected_bit_s:8,experiment:14,explain:14,explan:8,express:[8,9,16],extern:19,extra:[8,16,17,18,19],extra_attribut:14,extra_valu:14,f92d4800:12,fail:11,fals:[8,14,15],featur:[2,5,7,14],ff2d4800:12,field:[8,11,14,15,16,19],field_bit:14,field_bit_rang:14,field_decod:[8,16],field_element_index:14,field_extra:[8,19],field_nam:14,field_object:14,field_reg_type_:19,field_reg_type_add_1_imm12:19,field_reg_type_add_1_rd:19,field_reg_type_add_1_rn:19,field_result:8,fieldidconditionobject:[8,16],fieldinstructionconditionobjectdescript:8,file:[7,8,9,11,12,14],filter:11,find:[8,16],find_matched_instruct:8,find_matched_instructions_vector:8,fine:11,first:[8,16,19],fix:[2,3,5,8,14,16],fixed_bit:[8,16],fixed_bit_mask:[8,16],fixed_bit_nod:[8,16],fixed_bits_mask:[8,16],follow:[0,2,11,12,14,19],form:14,format:[0,5,8,11,12,19],from:[0,2,8,9,12,14],full:4,funct3:14,function_object:14,functionidconditionobject:[8,16],functioninstructionconditionobjectdescript:8,futur:[0,14],gcc:[11,14,19],gem:7,gener:[0,2,3,5,6,9,13,14,16,17],get:[11,15],git:[0,7],github:[0,5,7,10,11,14,19],given:[8,14],glanc:11,global:[14,17,19],good:11,googl:[2,3,4,5,11],grammar:[5,11],graphviz:[5,7],group:14,guid:[2,3,4,6,10,11],hand:0,handl:[11,15],has:[8,16],have:[5,8,11,13,16,19],header:7,helmesjo:7,help:4,here:[11,14,15,19],hex:[8,12],hold:[8,14],hook:[8,14],host:13,how:[3,6,11],html:7,htmlcov:7,http:[0,7],identifi:[2,15],ids:15,ignor:11,imm12:[0,11,14,19],imm:14,immedi:[7,8,14,16,19],immediateidconditionobject:[8,16],immediateinstructionconditionobjectdescript:8,implement:[0,5,8],improv:5,in_rang:[8,14,16],includ:[0,5,8,11,12,15,19],inclus:[8,14,16],inconsist:8,indata:12,independ:0,index:[8,10,14,16],inform:[8,11,14,17,19],inidcondit:[8,16],ininstructionconditiondescript:8,input:[8,11,12,15],inrangeidcondit:[8,16],inrangeinstructionconditiondescript:8,insert:14,inst:19,instal:[7,9],instanc:5,instead:[8,16],instruct:[0,8,9,12,13,15,16,17,18,19],instructin:8,instruction_decod:[8,16,17,19],instruction_encod:8,instruction_id:[11,15],instruction_id_max:15,instructionconditiondescript:8,instructionconditionobjectdescript:8,instructiondecod:[8,14,16,17],instructiondecodercondit:[8,16],instructiondecoderconditionobject:[8,16],instructiondecoderesult:8,instructiondecoderesult_:15,instructiondescript:8,instructionencodingdescript:8,instructionencodingelementdescript:8,instructionfielddecod:[8,16],instructionfielddecoderesult:8,instructionfieldencodingdescript:8,instructionid:[2,3,15],instructionid_add:2,instructionid_k_:15,instructionid_k_add:2,instructionid_k_add_immediate_a1:11,instructionid_k_push:15,instructionid_k_push_a1:11,instructionid_kunknown:[2,11,15],instructionsubfielddecod:[8,16],integ:[5,8,14,15],integr:[0,5,8,11],intern:[6,10],introduc:9,invalid:8,isn:[8,14,16],item:14,its:[5,8,11,14,16],itself:[8,16],jinja2:[5,19],json:[5,14],jsonschema:5,just:14,k_add:3,kcode:15,kdecodeerrorsmax:3,kei:14,kinstructionidmax:[2,3],kinstructionidmax_add:2,kmachinecod:[0,11],kunknown:3,kwarg:8,languag:[2,11],lark:5,lead:2,learn:0,learner:0,length:[8,13,16],length_of_encoding_el:[8,16],less:[2,8,14],let:11,librari:7,licens:9,like:[5,11,14,19],limit:[10,18],line:[5,8,10,11,18,19],list:[8,14,16],liter:[8,16],littl:[0,8,11,12,13,14,16,19],load:[5,8],load_mc_description_model:8,loaderror:8,logic:[8,14,16],logicalinstructionconditiondescript:8,longer:2,look:11,lsb:[8,11,14,16],lsb_in_field:[8,16],lsb_in_instruct:[8,16],machin:[0,8,11,12,16,17,18,19],machine_decod:[8,16,17],machinedecod:[8,16,17],machinedescript:8,macro:18,mai:19,main:[8,11],mainli:5,maintain:0,make:[2,5,7,8,11,19],make_mask:8,make_parent_directori:8,manag:5,map:14,mask:[8,16],match:[8,11,15,16],match_condit:[8,16],matrix:8,maximum:2,mcddecisionnod:[8,16],mcddecisiontre:[8,16],mcdecod:[2,3,4,8,9,11,12,14,15,16,17,19],mcdecoderdescript:8,mcdescript:8,mcfile:[8,12],mean:11,measur:5,member:[6,10],messag:8,might:14,minimum:11,mit:0,mixtur:14,model:[5,8,10,17,18,19],modif:[2,3,4],modul:[4,6,10],more:[3,5,9,11,19],msb:[8,11,14,16],msb_in_instruct:[8,16],much:3,multipl:[5,11,14],must:[4,8,11,13,14,16,19],mutual:14,name:[0,4,8,11,15,16,17,18,19],name_of_hook_funct:14,namespac:[2,8,15,16,17,19],namespace_prefix:[8,16,17],ndarrai:8,need:[11,19],next:9,nimm12:11,node:[8,16],non:8,none:[8,14],note:[8,12,14],now:11,nrd:11,number:[5,8,12,15,16],numpi:[5,8],object:[8,14,16],occur:8,offset:14,one:[8,14],onli:[5,8,12],oper:[8,14,16],opinion:2,option:[2,3,5,8,10,11,14,16,18,19],order:[8,12,14,16],oridcondit:[8,16],origin:[0,2,3,4],other:[2,3,11,12,13,14],otherwis:[8,15],out:[11,12,19],outdir:12,outfil:12,output:[8,11,12,19],output_directori:8,output_fil:8,over:11,overview:18,own:[11,19],packag:[4,7],pad:8,pad_trailing_zero:8,page:5,pain:0,paramet:[8,15],parent:8,pars:[5,8],parse_instruction_encod:8,part:[0,2,3,14],pass:[8,16],path:[7,8,12,14],pattern:[8,11,12,14],patternproperti:14,perform:5,pip:[0,4,7],place:[8,14],platform:7,point:8,portabl:2,posit:[8,16,18],possibl:12,prefix:[2,8,16,17,19],prevent:4,printf:[11,15],printinstruction_add:3,problem:12,process:[8,14],process_instruct:14,process_instruction_hook:8,produc:14,program:12,project:[2,3,4,5],prompt:14,properti:[8,14,16],provid:5,publish:5,push:15,push_1:[14,19],push_a1:11,push_instruct:14,put:[2,3,14,19],pyright:4,pytest:[5,7],python3:[0,7],python:[0,1,5,6,7,14],pyyaml:5,qualifi:2,quickstart:[9,10],r11:11,r13:11,rais:8,rang:[8,12,16],rational:[2,3,4],read:5,readabl:[2,14],readm:[9,10],reason:2,recommend:7,reflect:7,regist:[14,19],register_list:[11,14,15,19],rel:4,relat:[5,8,14,16],releas:14,remot:7,remov:[8,12,16,17],report:7,repres:14,request:[0,11,15],requir:[5,6,9],resolv:4,result:[0,5,8,11,14,15,16],riscv_decodeerrors_k_push:2,riscv_decodeerrors_push:2,riscv_decoderesult_push:2,riscv_kdecodeerrorsmax_push:2,riscv_printinstruction_push:2,root:[8,16,17],root_nod:[8,16],rst:5,rubi:7,rubygem:7,rule:1,run:[5,6,8,9,13,19],run_app:8,runtim:6,same:[4,8,11,14,19],satisfi:[8,16],scalar:14,schema:[5,8,18],scope:[14,17,19],script:5,search:[8,16],second:19,see:[0,2,3,4,11,14,17,19],separ:[2,14],sequenc:[11,14,17],set:[0,8,16],setbit_count:14,setup:6,setuptool:5,sever:[5,14],shell:5,shorthand:17,should:[2,5,8,11],show:[0,5,12],signatur:14,simplic:11,sinc:[8,16],size:8,skip:19,slash:14,some:[2,3,4,8,19],sooth:0,sourc:[5,7],specif:[0,5,8,10,11,19],specifi:[2,4,8,14,19],sphinx:5,split:[2,3,14],spreadsheet:11,src:[5,7,14],src_doc:[5,7],standard:12,start:[8,14,16],start_bit_in_instruct:[8,16],stdio:11,step:[0,11,19],str:[8,16],string:[8,12,14,16,17],string_length_for_byt:8,strongli:5,struct:15,structur:[14,19],style:[6,10],sub:[5,8,11,18],subclass:[8,16],subfield:[8,14,16],subfield_decod:[8,16],subfield_end:14,subfield_start:14,subject:[8,14,16],succeed:[0,8,11,15],sudo:7,support:[2,8,11,12,13,14,16,19],symbol:[2,3,8,14],syntax:[3,19],tabl:19,take:[14,19],taken:8,target:[2,8],tell:3,templat:[5,8,9,10,11,12,18],template_directori:8,templatedir:12,term:14,test:[0,5,6,8,11,14,16],than:[8,14,19],thei:[14,19],them:[2,3],theme:5,thi:[2,3,4,5,8,11,12,14,16,19],those:[4,19],threshold:[8,16],through:[8,16],time:[14,19],togeth:14,too:2,tool:[0,2,3,7],toolset:12,tough:0,trail:8,tree:[8,18],trim:8,trim_whitespac:8,tutori:[0,5,9,10,19],twice:4,two:[8,16],txt:7,type:[2,3,8,12,14,16,17,18,19],type_bit_length:[8,16],type_bit_s:[8,16],u0009:14,u000a:14,u000d:14,u0020:14,ubuntu:7,uint16_t:15,uint32_t:15,uint8:19,uint8_t:[0,11,15],underscor:[2,3],understand:[11,17,19],unintention:4,union:15,unit:5,unknown:[11,15],unmatch_condit:[8,16],unsign:15,usabl:5,usag:[9,12,18,19],use:[2,3,4,11,14,19],used:[5,8,12,14,16],useful:11,user:[0,5,8,10,11,12,14,16,17],user_templ:12,uses:[0,19],using:[11,14,15],util:5,valid:[5,8,12],valu:[5,8,11,14,16],value_end:[8,14,16],value_start:[8,14,16],variabl:[10,18,19],vector:[5,8],venv:7,version:[5,8,12,14,16,17],vertic:2,view:11,virtual:7,wai:[8,16,19],warn:5,what:[3,9],when:[8,12,14,16],where:[3,14,15],whether:8,which:[8,11,12,13,14,15],whitespac:8,who:9,wildcard:[12,14],wildlarva:[0,7],without:[7,15],word:[8,14],work:9,workflow:[5,8],write:[0,9],x92d4800:12,xx2d4800:12,xxx:14,xxxx:[0,11,14,19],yaml:[0,11,12,14,19],yoo:14,you:[2,3,4,7,11,14,19],your:[0,11,19],zero:8},titles:["README: mcdecoder","Coding style","C coding style","C++ coding style","Python coding style","Internal design","Documents for mcdecoder developers","Developer guides","Internal modules and members","User guides","The mcdecoder documentation","Quickstart tutorial","Command line option specification","Limitations","MC description specification","MC decoder API specification","MC decoder model specification","Template variable specification","Specifications","User templates"],titleterms:{"export":[8,12],"function":15,"import":[4,5],For:0,The:[10,11],__main__:8,__version__:8,about:0,add:[11,19],addit:[2,14],api:15,app:8,argument:12,arm:11,build:7,byteord:14,check:[11,12],checker:8,client:11,code:[1,2,3,4,11,19],command:12,comment:[2,3],common:[8,14],complex:14,condit:[14,16],core:8,creat:19,data:19,decis:16,decod:[7,11,14,15,16],defin:19,depend:5,descript:[11,14,19],design:5,detail:0,develop:[0,5,6,7],directori:5,document:[6,7,10],emul:[8,12],encod:11,enumer:2,environ:[5,7],equal:14,exampl:11,except:[2,3,4],express:[11,14],extern:5,extra:14,field_extra:14,file:[5,19],format:[2,14],from:11,gener:[7,8,11,12,19],guid:[7,9],how:7,immedi:11,includ:14,indic:10,instal:0,instruct:[11,14],intern:[5,8],introduc:11,languag:4,length:2,licens:0,limit:13,line:[2,12],machin:14,macro:15,match_condit:14,mcdecod:[0,5,6,7,10],member:8,model:16,modul:[5,8],more:0,name:[2,3,12,14],namespac:14,next:[11,19],option:12,other:5,overview:14,packag:5,posit:12,process_instruction_hook:14,push:11,python:4,quickstart:[0,11],rang:14,readm:0,requir:[0,7],rule:[2,3,4],run:[7,11],runtim:5,schema:14,set:14,setup:7,specif:[12,14,15,16,17,18],structur:5,style:[1,2,3,4],sub:12,tag:14,templat:[17,19],test:7,tree:16,tutori:11,type:15,unmatch_condit:14,usag:[0,15],user:[9,19],variabl:17,version:2,what:[11,19],who:0,work:11,write:11}})