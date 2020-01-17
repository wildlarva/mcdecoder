Search.setIndex({docnames:["README","dev_design","dev_docs","dev_guides","dev_modules","guides","index","quickstart","spec_commandline_options","spec_mc_desc","spec_mcdecoder_model","spec_template_var","specifications","user_templates"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,sphinx:56},filenames:["README.rst","dev_design.rst","dev_docs.rst","dev_guides.rst","dev_modules.rst","guides.rst","index.rst","quickstart.rst","spec_commandline_options.rst","spec_mc_desc.rst","spec_mcdecoder_model.rst","spec_template_var.rst","specifications.rst","user_templates.rst"],objects:{"mcdecoder.__main__":{main:[4,1,1,""]},"mcdecoder.app":{run_app:[4,1,1,""]},"mcdecoder.checker":{check:[4,1,1,""]},"mcdecoder.common":{bit_length_of_character:[4,1,1,""],convert_to_big_endian:[4,1,1,""],make_mask:[4,1,1,""],make_parent_directories:[4,1,1,""],pad_trailing_zeros:[4,1,1,""],string_length_for_byte:[4,1,1,""],trim_whitespace:[4,1,1,""]},"mcdecoder.core":{AndIdCondition:[4,2,1,""],BitRangeDescription:[4,2,1,""],DecodeContext:[4,2,1,""],DecodeContextVectorized:[4,2,1,""],EqualityIdCondition:[4,2,1,""],EqualityInstructionConditionDescription:[4,2,1,""],FieldIdConditionObject:[4,2,1,""],FieldInstructionConditionObjectDescription:[4,2,1,""],FunctionIdConditionObject:[4,2,1,""],FunctionInstructionConditionObjectDescription:[4,2,1,""],ImmediateIdConditionObject:[4,2,1,""],ImmediateInstructionConditionObjectDescription:[4,2,1,""],InIdCondition:[4,2,1,""],InInstructionConditionDescription:[4,2,1,""],InRangeIdCondition:[4,2,1,""],InRangeInstructionConditionDescription:[4,2,1,""],InstructionConditionDescription:[4,2,1,""],InstructionConditionObjectDescription:[4,2,1,""],InstructionDecodeResult:[4,2,1,""],InstructionDecoder:[4,2,1,""],InstructionDecoderCondition:[4,2,1,""],InstructionDecoderConditionObject:[4,2,1,""],InstructionDescription:[4,2,1,""],InstructionEncodingDescription:[4,2,1,""],InstructionEncodingElementDescription:[4,2,1,""],InstructionFieldDecodeResult:[4,2,1,""],InstructionFieldDecoder:[4,2,1,""],InstructionFieldEncodingDescription:[4,2,1,""],InstructionSubfieldDecoder:[4,2,1,""],LogicalInstructionConditionDescription:[4,2,1,""],MachineDecoder:[4,2,1,""],MachineDescription:[4,2,1,""],McDecoder:[4,2,1,""],McDecoderDescription:[4,2,1,""],McDescription:[4,2,1,""],McdDecisionNode:[4,2,1,""],McdDecisionTree:[4,2,1,""],OrIdCondition:[4,2,1,""],calc_instruction_bit_size:[4,1,1,""],create_mcdecoder_model:[4,1,1,""],decode_instruction:[4,1,1,""],find_matched_instructions:[4,1,1,""],find_matched_instructions_vectorized:[4,1,1,""],load_mc_description_model:[4,1,1,""],parse_instruction_encoding:[4,1,1,""]},"mcdecoder.core.AndIdCondition":{conditions:[4,3,1,""],type:[4,3,1,""]},"mcdecoder.core.BitRangeDescription":{end:[4,3,1,""],start:[4,3,1,""]},"mcdecoder.core.DecodeContext":{code16x1:[4,3,1,""],code16x2:[4,3,1,""],code32x1:[4,3,1,""],mcdecoder:[4,3,1,""]},"mcdecoder.core.DecodeContextVectorized":{code16x1_vec:[4,3,1,""],code16x2_vec:[4,3,1,""],code32x1_vec:[4,3,1,""],mcdecoder:[4,3,1,""]},"mcdecoder.core.EqualityIdCondition":{object:[4,3,1,""],operator:[4,3,1,""],subject:[4,3,1,""],type:[4,3,1,""]},"mcdecoder.core.EqualityInstructionConditionDescription":{object:[4,3,1,""],operator:[4,3,1,""],subject:[4,3,1,""]},"mcdecoder.core.FieldIdConditionObject":{element_index:[4,3,1,""],field:[4,3,1,""],type:[4,3,1,""]},"mcdecoder.core.FieldInstructionConditionObjectDescription":{element_index:[4,3,1,""],field:[4,3,1,""]},"mcdecoder.core.FunctionIdConditionObject":{"function":[4,3,1,""],argument:[4,3,1,""],type:[4,3,1,""]},"mcdecoder.core.FunctionInstructionConditionObjectDescription":{"function":[4,3,1,""],argument:[4,3,1,""]},"mcdecoder.core.ImmediateIdConditionObject":{type:[4,3,1,""],value:[4,3,1,""]},"mcdecoder.core.ImmediateInstructionConditionObjectDescription":{value:[4,3,1,""]},"mcdecoder.core.InIdCondition":{subject:[4,3,1,""],type:[4,3,1,""],values:[4,3,1,""]},"mcdecoder.core.InInstructionConditionDescription":{subject:[4,3,1,""],values:[4,3,1,""]},"mcdecoder.core.InRangeIdCondition":{subject:[4,3,1,""],type:[4,3,1,""],value_end:[4,3,1,""],value_start:[4,3,1,""]},"mcdecoder.core.InRangeInstructionConditionDescription":{subject:[4,3,1,""],value_end:[4,3,1,""],value_start:[4,3,1,""]},"mcdecoder.core.InstructionDecodeResult":{decoder:[4,3,1,""],field_results:[4,3,1,""]},"mcdecoder.core.InstructionDecoder":{encoding_element_bit_length:[4,3,1,""],extras:[4,3,1,""],field_decoders:[4,3,1,""],fixed_bits:[4,3,1,""],fixed_bits_mask:[4,3,1,""],length_of_encoding_elements:[4,3,1,""],match_condition:[4,3,1,""],name:[4,3,1,""],type_bit_size:[4,3,1,""],unmatch_condition:[4,3,1,""]},"mcdecoder.core.InstructionDescription":{extras:[4,3,1,""],field_extras:[4,3,1,""],format:[4,3,1,""],match_condition:[4,3,1,""],name:[4,3,1,""],unmatch_condition:[4,3,1,""]},"mcdecoder.core.InstructionEncodingDescription":{elements:[4,3,1,""]},"mcdecoder.core.InstructionEncodingElementDescription":{fields:[4,3,1,""]},"mcdecoder.core.InstructionFieldDecodeResult":{decoder:[4,3,1,""],value:[4,3,1,""]},"mcdecoder.core.InstructionFieldDecoder":{extras:[4,3,1,""],name:[4,3,1,""],subfield_decoders:[4,3,1,""],type_bit_size:[4,3,1,""]},"mcdecoder.core.InstructionFieldEncodingDescription":{bit_ranges:[4,3,1,""],bits_format:[4,3,1,""],name:[4,3,1,""]},"mcdecoder.core.InstructionSubfieldDecoder":{end_bit_in_field:[4,3,1,""],end_bit_in_instruction:[4,3,1,""],index:[4,3,1,""],mask:[4,3,1,""],start_bit_in_instruction:[4,3,1,""]},"mcdecoder.core.LogicalInstructionConditionDescription":{conditions:[4,3,1,""],operator:[4,3,1,""]},"mcdecoder.core.MachineDecoder":{byteorder:[4,3,1,""],extras:[4,3,1,""]},"mcdecoder.core.MachineDescription":{byteorder:[4,3,1,""],extras:[4,3,1,""]},"mcdecoder.core.McDecoder":{decision_trees:[4,3,1,""],extras:[4,3,1,""],instruction_decoders:[4,3,1,""],machine_decoder:[4,3,1,""],namespace_prefix:[4,3,1,""]},"mcdecoder.core.McDecoderDescription":{namespace:[4,3,1,""]},"mcdecoder.core.McDescription":{decoder:[4,3,1,""],extras:[4,3,1,""],instructions:[4,3,1,""],machine:[4,3,1,""]},"mcdecoder.core.McdDecisionNode":{all_nodes:[4,4,1,""],arbitrary_bit_node:[4,3,1,""],fixed_bit_nodes:[4,3,1,""],index:[4,3,1,""],instructions:[4,3,1,""],mask:[4,3,1,""]},"mcdecoder.core.McdDecisionTree":{encoding_element_bit_length:[4,3,1,""],length_of_encoding_elements:[4,3,1,""],root_node:[4,3,1,""]},"mcdecoder.core.OrIdCondition":{conditions:[4,3,1,""],type:[4,3,1,""]},"mcdecoder.emulator":{emulate:[4,1,1,""]},"mcdecoder.exporter":{"export":[4,1,1,""]},"mcdecoder.generator":{generate:[4,1,1,""]},mcdecoder:{__main__:[4,0,0,"-"],app:[4,0,0,"-"],checker:[4,0,0,"-"],common:[4,0,0,"-"],core:[4,0,0,"-"],emulator:[4,0,0,"-"],exporter:[4,0,0,"-"],generator:[4,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","function","Python function"],"2":["py","class","Python class"],"3":["py","attribute","Python attribute"],"4":["py","method","Python method"]},objtypes:{"0":"py:module","1":"py:function","2":"py:class","3":"py:attribute","4":"py:method"},terms:{"002d4800":8,"00482de9":8,"092d4800":8,"0b0":7,"0b100":7,"0b1011":7,"0b1101":7,"0b1110":7,"0b1111":[7,9],"0th":[4,10],"0x0":7,"0x04":[0,7],"0x4":7,"0x8d":[0,7],"0xb":7,"0xb0":[0,7],"0xd":7,"0xe":7,"0xe2":[0,7],"0xf":9,"15th":9,"1x10":8,"boolean":4,"break":7,"byte":[4,8,10],"case":7,"char":7,"class":[4,10],"const":13,"default":[4,7,8],"enum":9,"export":[1,2,7],"final":13,"function":[4,7,9,10],"int":[0,4,7,10],"return":[1,4,7],"static":0,"switch":[3,7],"true":4,"void":7,"while":4,AND:[4,10],And:13,For:[5,7],Its:7,One:9,The:[4,8,9,10],These:9,Use:[0,7,13],Used:1,Uses:[1,4,10],__main__:[1,2],_encod:[4,10],_instruct:9,_start_bit:[4,10],about:[1,5,7,11,13],abov:3,access:13,accord:[1,7,8],act:8,activ:3,actual:0,add:5,add_1:[9,13],add_immediate_a1:[0,7],add_instruct:9,added:4,addit:[4,7,12,13],additionalproperti:9,adjac:9,after:3,against:[1,4],align:4,all:[1,4,7,9],all_nod:[4,10],allow:13,also:9,alwai:[4,10],analyz:0,andidcondit:[4,10],ani:[4,9,10,11,13],anoth:[4,8,9],anywher:9,api:7,app:[1,2,7],appli:[3,4,10],applic:4,approach:0,apt:3,arbitrari:[4,10],arbitrary_bit_nod:[4,10],arch_typ:[9,13],architectur:13,argpars:1,argument:[4,7,9,10,12],argv:4,arm:[0,9,13],arm_const:13,arrai:9,assembl:7,asterisk:9,athril:[0,4],attribut:[4,10,13],automat:1,bar:9,base:[1,4,8,9,10],basic:0,befor:[7,9],behavior:[7,9],below:[0,7,9,13],between:9,big:[4,8,9,10],billion:1,bin:3,binari:[0,4,8],bit:[4,7,9,10],bit_length_of_charact:4,bit_pattern:4,bit_rang:4,bit_siz:4,bitrangedescript:4,bits_format:4,bool:4,both:1,build:[1,2],byteord:[0,4,7,8,10,13],calc_instruction_bit_s:4,calcul:[1,4],call:[4,7,9,10,13],callback:7,can:[7,9,13],certain:[1,7,8],chang:3,charact:[4,8,9],check:[0,1,4,5,13],checker:[1,2],child:[4,10],choic:8,clean:3,client:[0,5],clock:[9,13],clone:[0,3],code16x1:4,code16x1_vec:4,code16x2:4,code16x2_vec:4,code32x1:4,code32x1_vec:4,code:[0,1,4,5,8,9,10,11],code_id:7,coincid:7,com:[0,3],combin:[4,9,10],comma:9,command:[1,4,6,7,12,13],common:[1,2],compil:[7,9,13],conan:1,cond:[0,7,9,13],condit:[4,7,10],consid:1,consist:9,constant:13,construct:9,contain:[4,13],content:[1,2,5,6,7,9,12,13],context:4,convers:4,convert:[1,4],convert_to_big_endian:4,core:[1,2,7,10],correspond:[4,8],count:9,cpu:[0,7],creat:[1,3,4,5,7],create_mcdecoder_model:4,csv:[4,7,8],ctest:[1,3],cumbersom:0,current:[4,8],custom:7,data:[0,4,5,8,10,11,12],decid:[4,10],decis:[4,10],decision_tre:[4,10],decod:[0,1,2,4,5,6,8,11,12,13],decode_instruct:4,decodecontext:4,decodecontextvector:4,decoded_cod:[0,7],defin:[0,1,4,5,7,8,10,11,12],depend:9,depth:[4,10],descend:[4,10],describ:[4,12],descript:[1,4,5,6,8,11,12],design:[2,6,13],dest:9,detail:[5,7,13],detect:8,develop:[5,6],diagram:1,dict:[4,10],dictionari:[4,10],did:7,directoi:8,directori:[3,4,8,13],dispatch:1,doc:1,document:[0,1,13],doe:[1,4,9],don:13,doubl:9,duplic:8,e28db004:7,e92d4800:8,each:[1,4,7,10],element:[4,7,9,10,11],element_index:[4,10],els:[7,13],emul:[0,1,2,7],encod:[4,5,10],encoding_element_bit_length:[4,10],end:[4,9,10],end_bit_in_field:[4,10],end_bit_in_instruct:[4,10],endfor:13,endian:[4,8,9],endif:13,entri:4,entrypoint:1,env:3,environ:2,equal:[4,10],equalityidcondit:[4,10],equalityinstructionconditiondescript:4,error:[4,9],etc:[0,1,4,9],exampl:[1,5,9,13],excel:7,exclus:9,execut:[4,7],exist:13,exit:4,expect:4,expected_bit_s:4,explain:9,express:[4,5,10],extern:13,extra:[4,10,11,12,13],f92d4800:8,fail:7,fals:[4,9],featur:1,ff2d4800:8,field:[4,7,10,13],field_bit:9,field_bit_rang:9,field_decod:[4,10,13],field_element_index:9,field_extra:[4,13],field_nam:9,field_object:9,field_reg_type_:13,field_reg_type_add_1_imm12:13,field_reg_type_add_1_rd:13,field_reg_type_add_1_rn:13,field_result:4,fieldidconditionobject:[4,10],fieldinstructionconditionobjectdescript:4,file:[4,5,7,8],filter:7,find:[4,10],find_matched_instruct:4,find_matched_instructions_vector:4,fine:7,first:[4,10,13],fix:[4,9,10],fixed_bit:[4,10],fixed_bit_nod:[4,10],fixed_bits_mask:[4,10],follow:[0,7,8,9,13],format:[0,1,4,7,8,13],from:[0,4,5,8,9],funct3:9,function_object:9,functionidconditionobject:[4,10],functioninstructionconditionobjectdescript:4,futur:0,gcc:[7,9,13],gener:[0,1,2,5,10,11],get:7,git:[0,3],github:[0,1,3,7,9,13],given:[4,9],glanc:7,global:[11,12,13],good:7,googl:[1,7],grammar:[1,7],graphviz:[1,3],group:9,guid:[2,6,7],hand:0,has:[4,10],have:[1,4,7,10,13],here:[7,9],hex:[4,8],hold:[4,9],how:[2,7],html:3,http:[0,3],ignor:7,imm12:[0,7,9,13],imm:9,immedi:[3,4,9,10,13],immediateidconditionobject:[4,10],immediateinstructionconditionobjectdescript:4,implement:[0,1,4],improv:1,in_rang:[4,9,10,13],includ:[0,1,4,7,8,13],inclus:[4,9,10],independ:0,index:[4,6,9,10],inform:[4,7,11,12,13],inidcondit:[4,10],ininstructionconditiondescript:4,input:[4,7,8],inrangeidcondit:[4,10],inrangeinstructionconditiondescript:4,insert:9,inst:13,instal:[3,5],instanc:1,instruct:[0,4,5,8,10,11,12,13],instructin:4,instruction_decod:[4,10,11,13],instruction_encod:4,instructionconditiondescript:4,instructionconditionobjectdescript:4,instructiondecod:[4,10,11],instructiondecodercondit:[4,10],instructiondecoderconditionobject:[4,10],instructiondecoderesult:4,instructiondescript:4,instructionencodingdescript:4,instructionencodingelementdescript:4,instructionfielddecod:[4,10],instructionfielddecoderesult:4,instructionfieldencodingdescript:4,instructionsubfielddecod:[4,10],integ:[1,4,9],integr:[0,1,4,7],intern:[2,6],introduc:5,isn:[4,9,10],item:9,its:[1,4,7,9,10],itself:[4,10],jinja2:[1,13],json:[1,9],jsonschema:1,just:9,kei:9,languag:7,lark:1,learn:0,learner:0,length:[4,10],length_of_encoding_el:[4,10],less:[4,9],let:7,librari:3,like:[1,7,9,13],line:[1,4,6,7,12,13],list:[4,9,10],liter:[4,10],littl:[0,4,7,8,9,10,13],load:[1,4],load_mc_description_model:4,logic:[4,9,10],logicalinstructionconditiondescript:4,look:7,lsb:[4,7,9,10],m2r:1,machin:[0,4,7,8,10,11,12,13],machine_cod:[0,7],machine_decod:[4,10,11,13],machinedecod:[4,10,11],machinedescript:4,mai:13,main:[4,7],maintain:0,make:[1,3,4,7,13],make_mask:4,make_parent_directori:4,manag:1,map:9,mask:[4,10],match:[4,7,10],match_condit:[4,10,13],matrix:4,mcddecisionnod:[4,10],mcddecisiontre:[4,10],mcdecod:[4,5,7,8,10,11,13],mcdecoderdescript:4,mcdescript:4,mcfile:[4,8],mcfile_path:4,mean:7,member:[2,6],minimum:7,mixtur:9,model:[1,4,6,11,12,13],modul:[2,6],more:[1,5,7,13],msb:[4,7,9,10],multipl:[1,7],must:[4,7,10,13],mutual:9,name:[0,4,7,10,11,13],namespac:[4,10,11,13],namespace_prefix:[4,10,11],ndarrai:4,need:[7,13],next:5,node:[4,10],non:4,none:[4,10],nop:7,note:[4,8,9],now:7,number:[4,10],numpi:[1,4],object:[4,9,10],offset:9,one:[4,9],onli:[1,4,8],op_decode_max:7,op_exec_:7,op_exec_add_immediate_a1:7,op_exec_push_a1:7,op_pars:[0,7],opcodeid_add_immediate_a1:7,opcodeid_push_a1:7,opdecodedcodetyp:[0,7],oper:[4,9,10],operationcodetyp:[0,7],option:[1,4,6,7,9,10,12,13],optyp:[0,7],order:[4,8,10],oridcondit:[4,10],origin:0,other:[3,7,8,9],otherwis:4,out:[7,8,13],outdir:8,outfil:8,output:[4,7,8,13],output_directori:4,output_fil:4,over:7,overview:12,own:[7,13],pad:4,pad_trailing_zero:4,page:1,pain:0,paramet:4,parent:4,pars:[1,4],parse_instruction_encod:4,part:[0,9],pass:[4,10],path:[3,4,8,9],pattern:[4,7,8,9],patternproperti:9,perform:1,pip:[0,3],place:[4,9],point:4,posit:[4,10,12],possibl:8,prefix:[4,10,11,13],printf:7,problem:8,produc:9,project:1,prompt:9,properti:[4,9,10],provid:1,publish:1,push_1:[9,13],push_a1:7,push_instruct:9,put:13,pytest:[1,3],python3:[0,3],python:[0,1,3],pyyaml:1,quickstart:[5,6],r11:7,r13:7,rang:[4,8,10],read:1,readabl:9,readm:[1,5,6],reflect:3,regist:[9,13],register_list:[7,9,13],relat:[1,4,9,10],repres:9,requir:[1,2,5],result:[0,1,4,7,9,10],root:[4,10,11],root_nod:[4,10],rst:1,run:[1,2,4,5,13],run_app:4,runtim:2,same:[4,7,9,13],satisfi:[4,10],scalar:9,schema:[1,4,12],scope:[11,12,13],script:1,search:[4,10],second:13,see:[0,7,9,11,13],separ:9,sequenc:[7,9,11],set:[0,4,10],setbit_count:9,setup:2,setuptool:1,sever:[1,9],shell:1,shorthand:11,should:[1,4,7],show:[0,1],simplic:7,size:[4,10],skip:13,slash:9,some:[4,13],sooth:0,sourc:[1,3],specif:[0,4,6,7,13],specifi:[4,9,13],sphinx:1,spreadsheet:7,src:[1,9],src_doc:[1,3],start:[4,9,10],start_bit_in_instruct:[4,10],stdio:7,step:[0,7,13],str:[4,10],string:[4,8,9,10,11],string_length_for_byt:4,strongli:1,struct:7,structur:[9,13],stub:7,sub:[1,4,7,12],subclass:[4,10],subfield:[4,9,10],subfield_decod:[4,10],subfield_end:9,subfield_start:9,subject:[4,9,10],succeed:[4,7],sudo:3,support:[4,7,8,9,10,13],symbol:4,syntax:13,tabl:13,tag:9,take:[9,13],taken:4,target:4,targetcor:7,templat:[1,4,5,6,7,8,12],template_directori:4,templatedir:8,term:9,test:[0,1,2,4,7,9,10],than:[4,9,13],thei:[9,13],theme:1,thi:[1,4,7,8,9,10,13],those:13,threshold:[4,10],through:[4,10],time:[9,13],togeth:9,tool:[0,3],toolset:8,tough:0,trail:4,tree:[4,10],trim:4,trim_whitespac:4,tutori:[0,1,5,6,13],two:[4,10],txt:3,type:[4,9,10,11,13],type_bit_s:[4,10],u0020u0009u000au000d:9,ubuntu:3,uint16:[0,7],uint8:[0,13],understand:[7,11,13],unmatch_condit:[4,10,13],unsign:7,usabl:1,usag:[5,8,13],use:[7,9,13],used:[1,4,9,10],useful:7,user:[0,4,6,7,8,10,11,12],user_templ:8,uses:13,using:[7,9],util:1,valid:[1,4,8],valu:[1,4,7,9,10],value_end:[4,9,10],value_start:[4,9,10],variabl:[6,12,13],vector:[1,4],venv:3,version:9,view:7,virtual:3,wai:[4,10,13],what:5,when:[4,8,9,10],where:9,whether:4,which:[4,7,8,9],whitespac:4,who:5,wildcard:[8,9],wildlarva:[0,3],word:[4,9],work:5,workflow:[1,4],write:[0,5],x92d4800:8,xx2d4800:8,xxx:9,xxxx:[0,7,9,13],yaml:[0,7,8,9,13],you:[3,7,9,13],your:[0,7,13],zero:4},titles:["README: mcdecoder","Internal design","Documents for mcdecoder developers","Developer guides","Internal modules and members","User guides","mcdecoder documentation","Quickstart tutorial","Command line option specification","MC description specification","MC decoder model specification","Template variable specification","Specifications","User templates"],titleterms:{"byte":9,"export":[4,8],"import":1,For:0,The:7,__main__:4,about:0,add:[7,13],addit:9,app:4,appli:9,argument:8,arm:7,build:3,byteord:9,check:[7,8],checker:4,client:7,code:[7,13],command:8,common:[4,9],complex:9,condit:9,core:4,creat:13,data:[9,13],decod:[3,7,9,10],defin:[9,13],depend:1,describ:9,descript:[7,9,13],design:1,detail:0,develop:[0,1,2,3],directori:1,document:[2,3,6],doesn:9,each:9,emul:[4,8],encod:[7,9],environ:[1,3],equal:9,exampl:7,express:[7,9],extern:1,extra:9,field:9,field_extra:9,file:[1,9,13],format:9,from:7,gener:[3,4,7,8,9,13],global:9,guid:[3,5],how:3,immedi:7,includ:9,indic:6,inform:9,instal:0,instruct:[7,9],intern:[1,4],introduc:7,line:8,machin:9,match_condit:9,mcdecod:[0,1,2,3,6],member:4,model:10,modul:[1,4],more:0,multipl:9,name:[8,9],namespac:9,next:[7,13],option:8,order:9,other:1,overview:9,packag:1,posit:8,push:7,quickstart:[0,7],rang:9,readm:0,requir:[0,3],run:[3,7],runtim:1,schema:9,scope:9,set:9,setup:3,specif:[8,9,10,11,12],split:9,structur:1,sub:8,symbol:9,templat:[11,13],test:3,tutori:7,unmatch_condit:9,usag:0,user:[5,9,13],variabl:11,what:[7,13],who:0,work:7,write:7}})