Search.setIndex({docnames:["config","index","project_rst/annotator_rst/annotator","project_rst/annotator_rst/forms","project_rst/annotator_rst/helpers","project_rst/annotator_rst/routes","project_rst/generator","project_rst/models","project_rst/project","project_rst/user_rst/forms","project_rst/user_rst/helpers","project_rst/user_rst/routes","project_rst/user_rst/user","project_rst/validators","templates"],envversion:{"sphinx.domains.c":1,"sphinx.domains.changeset":1,"sphinx.domains.citation":1,"sphinx.domains.cpp":1,"sphinx.domains.javascript":1,"sphinx.domains.math":2,"sphinx.domains.python":1,"sphinx.domains.rst":1,"sphinx.domains.std":1,"sphinx.ext.intersphinx":1,"sphinx.ext.viewcode":1,sphinx:56},filenames:["config.rst","index.rst","project_rst/annotator_rst/annotator.rst","project_rst/annotator_rst/forms.rst","project_rst/annotator_rst/helpers.rst","project_rst/annotator_rst/routes.rst","project_rst/generator.rst","project_rst/models.rst","project_rst/project.rst","project_rst/user_rst/forms.rst","project_rst/user_rst/helpers.rst","project_rst/user_rst/routes.rst","project_rst/user_rst/user.rst","project_rst/validators.rst","templates.rst"],objects:{"":{config:[0,0,0,"-"]},"config.Config":{init_app:[0,2,1,""]},"project.__init__":{create_app:[8,4,1,""],init_extensions:[8,4,1,""],register_blueprints:[8,4,1,""]},"project.annotator":{__init__:[2,0,0,"-"],account:[5,0,0,"-"],annotation:[5,0,0,"-"],forms:[3,0,0,"-"],helpers:[4,0,0,"-"],views:[5,0,0,"-"]},"project.annotator.account":{login:[5,4,1,""]},"project.annotator.annotation":{batch:[5,4,1,""],hit:[5,4,1,""]},"project.annotator.forms":{AnnoCheckinForm:[3,1,1,""],TupleForm:[3,1,1,""]},"project.annotator.forms.AnnoCheckinForm":{keyword:[3,5,1,""],name:[3,5,1,""],validate:[3,2,1,""]},"project.annotator.forms.TupleForm":{best_item:[3,5,1,""],worst_item:[3,5,1,""]},"project.annotator.helpers":{batches_list:[4,4,1,""]},"project.annotator.views":{project:[5,4,1,""]},"project.generator":{BaseGenerator:[6,1,1,""],DataGenerator:[6,1,1,""],ScoreGenerator:[6,1,1,""]},"project.generator.BaseGenerator":{frequencies:[6,5,1,""],get_frequency:[6,2,1,""]},"project.generator.DataGenerator":{batch_size:[6,5,1,""],batches:[6,5,1,""],factor:[6,5,1,""],generate_batches:[6,2,1,""],generate_data:[6,2,1,""],generate_items:[6,2,1,""],generate_tuples:[6,2,1,""],items:[6,5,1,""],minimum:[6,5,1,""],num_iter:[6,5,1,""],tuple_size:[6,5,1,""],tuples:[6,5,1,""]},"project.generator.ScoreGenerator":{best:[6,5,1,""],frequencies:[6,5,1,""],scoring:[6,2,1,""],worst:[6,5,1,""]},"project.models":{Annotator:[7,1,1,""],Batch:[7,1,1,""],Data:[7,1,1,""],Item:[7,1,1,""],Project:[7,1,1,""],Tuple:[7,1,1,""],User:[7,1,1,""]},"project.models.Annotator":{batches:[7,5,1,""],get_id:[7,2,1,""],id:[7,5,1,""],keyword:[7,5,1,""],name:[7,5,1,""],project:[7,5,1,""],project_id:[7,5,1,""]},"project.models.Batch":{hit_id:[7,5,1,""],id:[7,5,1,""],keyword:[7,5,1,""],project:[7,5,1,""],project_id:[7,5,1,""],size:[7,5,1,""]},"project.models.Data":{anno_id:[7,5,1,""],annotator:[7,5,1,""],best_id:[7,5,1,""],id:[7,5,1,""],tuple_:[7,5,1,""],tuple_id:[7,5,1,""],worst_id:[7,5,1,""]},"project.models.Item":{id:[7,5,1,""],item:[7,5,1,""]},"project.models.Project":{anno_number:[7,5,1,""],best_def:[7,5,1,""],description:[7,5,1,""],id:[7,5,1,""],mturk:[7,5,1,""],n_items:[7,5,1,""],name:[7,5,1,""],p_name:[7,5,1,""],user:[7,5,1,""],user_id:[7,5,1,""],worst_def:[7,5,1,""]},"project.models.Tuple":{batch:[7,5,1,""],batch_id:[7,5,1,""],id:[7,5,1,""],items:[7,5,1,""]},"project.models.User":{check_password:[7,2,1,""],email:[7,5,1,""],get_id:[7,2,1,""],id:[7,5,1,""],password:[7,5,1,""],username:[7,5,1,""]},"project.user":{__init__:[12,0,0,"-"],account:[11,0,0,"-"],forms:[9,0,0,"-"],helpers:[10,0,0,"-"],inputs:[11,0,0,"-"],outputs:[11,0,0,"-"],views:[11,0,0,"-"]},"project.user.account":{login:[11,4,1,""],logout:[11,4,1,""],signup:[11,4,1,""]},"project.user.forms":{LoginForm:[9,1,1,""],ProjectInformationForm:[9,1,1,""],RegisterForm:[9,1,1,""]},"project.user.forms.LoginForm":{password:[9,5,1,""],remember:[9,5,1,""],username:[9,5,1,""],validate:[9,2,1,""]},"project.user.forms.ProjectInformationForm":{anno_number:[9,5,1,""],aws_access_key_id:[9,5,1,""],aws_secret_access_key:[9,5,1,""],best_def:[9,5,1,""],description:[9,5,1,""],duration_unit:[9,5,1,""],hit_duration:[9,5,1,""],keywords:[9,5,1,""],lifetime:[9,5,1,""],lifetimeunit:[9,5,1,""],mturk:[9,5,1,""],name:[9,5,1,""],reward:[9,5,1,""],upload:[9,5,1,""],validate_upload:[9,2,1,""],worst_def:[9,5,1,""]},"project.user.forms.RegisterForm":{email:[9,5,1,""],password:[9,5,1,""],username:[9,5,1,""],validate_username:[9,2,1,""]},"project.user.helpers":{convert_into_seconds:[10,4,1,""],generate_keyword:[10,4,1,""],is_not_current_user:[10,4,1,""],upload_file:[10,4,1,""]},"project.user.inputs":{upload_project:[11,4,1,""]},"project.user.outputs":{get_keywords:[11,4,1,""],get_report:[11,4,1,""],get_scores:[11,4,1,""]},"project.user.views":{main:[11,4,1,""],profile:[11,4,1,""],project:[11,4,1,""]},"project.validators":{InputValid:[13,1,1,""],NotEqualTo:[13,1,1,""],Unique:[13,1,1,""],allowed_file:[13,4,1,""]},config:{Config:[0,1,1,""],DevelopmentConfig:[0,1,1,""],TestingConfig:[0,1,1,""],config:[0,3,1,""]},project:{__init__:[8,0,0,"-"],generator:[6,0,0,"-"],models:[7,0,0,"-"],validators:[13,0,0,"-"]}},objnames:{"0":["py","module","Python module"],"1":["py","class","Python class"],"2":["py","method","Python method"],"3":["py","data","Python data"],"4":["py","function","Python function"],"5":["py","attribute","Python attribute"]},objtypes:{"0":"py:module","1":"py:class","2":"py:method","3":"py:data","4":"py:function","5":"py:attribute"},terms:{"boolean":7,"case":7,"char":10,"class":[0,3,6,7,9,13],"default":[0,4,6,9,10,13],"float":6,"function":[1,2,6,8,12,13],"import":0,"int":[4,5,6,10],"new":[11,14],"return":[4,5,6,7,8,10,11,13],"true":[0,7,9,10,13],AWS:[0,9],BWS:[6,11],For:[0,1],The:[1,6],Use:[7,13],With:2,__init__:8,about:6,accept:6,access:[0,7,9,10],account:[1,2,9,10,12],acronym:10,actual:10,after:6,aggress:6,all:[0,2,5,6,10,11,13,14],allow:[9,10,13],allowed_fil:13,alreadi:13,also:1,amazon:[0,1],anno_id:7,anno_numb:[7,9],annocheckinform:3,annoi:6,annot:[1,3,4,6,7,8,9,10,11],anoth:[10,13],answer:3,api:1,app:[0,8],appear:6,applic:[0,1,6,7,14],approxim:6,ascii_lett:10,ask:10,attribut:[6,10,13],authent:10,automat:7,avail:0,availab:9,avoid:7,aws_access_key_id:[0,9],aws_secret_access_kei:[0,9],base:[0,6,8],base_dir:0,basegener:6,batch:[2,4,5,6,7,10,11,14],batch_id:[4,5,7,14],batch_nam:4,batch_siz:6,batches_list:4,belong:7,besid:1,best:[3,6,7,9],best_def:[7,9],best_id:7,best_item:3,bind:8,blueprint:[2,8,12],bool:[0,7,10,13],booleanfield:9,bootstrap4:1,bore:6,bufferedread:6,button:4,calcul:[6,7,11],call:[6,13],can:[0,6],chang:6,charact:[9,10],check:[3,7,9,13],check_password:7,check_password_hash:7,choic:[3,14],chosen:7,code:[1,6],collect:[6,11],column:13,condit:10,config:[0,8],config_env:8,configur:[1,8],contain:[6,10],content:8,convert:10,convert_into_second:10,correspond:[4,5],count:6,counter:6,creat:[4,6,7,11,14],create_app:8,credenti:0,criteria:6,crowdsourc:[0,1],csrf:0,css:1,csv:13,current:[10,11],current_nam:10,current_us:10,dai:10,data:[2,6,7,9,11,13],databas:[0,7,13],datagener:[6,10],deal:[4,10],debug:0,decid:6,defin:[0,2,3,4,5,7,8,9,11,12],definit:[7,9],descendingli:6,describ:9,descript:[7,9],develop:[0,1],developmentconfig:0,dict:6,dictionari:6,differ:[0,6,14],digit:10,direct:5,directori:0,document:1,durat:[9,10],duration_unit:9,dure:[0,6],dynam:1,each:[4,5,6,7,8,9,10,11,14],east:0,element:13,els:[6,7,10,11,13],email:[7,9,11],emerg:[5,11],enabl:0,endpoint:[0,7,11],environ:[0,8],equalto:13,error:[5,11],exampl:[4,6,7,10,13],excit:6,exist:13,expect:[7,9],extend:[0,3,6,7,9],extens:[1,8,9,13],factor:6,fail:13,fals:[0,7,10,13],fantast:6,fewer:[6,10],field:[11,13],fieldnam:13,file:[6,9,10,11,13],file_nam:6,filenam:13,filestorag:[6,10],first:3,flask:[1,8],flask_env:0,flask_sqlalchemi:7,flaskform:[3,9],follow:6,form:[0,1,2,6,8,12,13],format:7,formdata:[3,9],formula:6,frequenc:6,from:[5,6,7,11],gener:[1,8,10],generate_batch:6,generate_data:6,generate_item:6,generate_keyword:10,generate_password_hash:7,generate_tupl:6,get:[6,7,12],get_frequ:6,get_id:7,get_keyword:11,get_report:11,get_scor:11,given:[3,4,5,6,7,9,10],global:0,handl:6,has:[9,13],hash:7,have:[7,9,13],helper:[1,2,8,12],his:3,hit:[5,9,11,14],hit_dur:9,hit_id:[5,7,14],homepag:[11,14],hour:10,how:7,html:[0,1,14],iam:[0,9],ident:6,includ:[1,6],independ:6,index:[1,14],indiffer:6,inform:[11,14],init_app:0,init_extens:8,initi:0,input:[0,1,6,12,13],inputvalid:13,insid:[3,4,5,6,9,10,13],instanc:8,instead:0,integ:7,integerfield:9,integr:1,interest:6,invalid:[5,11,13],is_not_current_us:10,item:[3,6,7,9,10,11],iter:6,its:[1,14],javascript:1,jinja2:1,joy:6,k_length:10,kei:[0,9],keyword:[3,5,7,9,10,11,14],kwarg:[3,9],label:9,later:10,least:11,len:6,length:10,lifetim:9,lifetimeunit:9,like:13,link:0,list:[4,6,10,13],local:[0,2,5,7,11],localproxi:10,log:[3,7,10,11],login:[2,3,5,7,8,9,10,11,12,14],loginform:9,logout:11,main:[1,2,11,12],mainli:[0,1],make:13,manag:[1,2,7,8,12],mani:7,mean:10,mechan:[2,7,9,11,14],meet:[6,10],meeth:10,messag:[5,11,13],method:[6,7],min:10,minimum:6,minut:10,model:[1,8,13],modif:0,modul:[0,1,3,4,5,6,7,9,10,11,13],month:[9,10],more:[6,7],most:1,mostli:13,movie_reviews_exampl:6,mturk:[2,5,7,9,14],mturk_show_up_url:0,mturk_url:0,multi:[7,8],multipl:14,multiplefilefield:9,n_batch:4,n_item:7,n_tupl:6,name:[3,4,5,7,9,10,11,13],necessari:6,none:[0,7,10,13],normal:6,notequalto:13,num_it:6,number:[4,6,7,9,10],object:[0,3,6,9,10,13],occur:6,one:[3,6,7,9,11],onli:[6,7,9],open:6,option:[6,7,9],orm:6,other:10,other_fieldnam:13,output:[1,12],outsid:6,overrid:[3,7,9],overwritten:13,p_name:[5,7,11],packag:8,page:[0,1,10,11,14],pair:6,paramet:[0,4,5,6,7,8,10,11,13],part:7,password:[7,9,11],passwordfield:[3,9],person:3,platform:[0,1,11],prepar:6,problem:[4,10],product:0,profil:[10,11,12,14],project:[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14],project_id:7,project_nam:14,projectinformationform:9,provid:[6,9,10,11,13],pseudo:[3,5],pseudonam:[3,7],python3:1,question:[3,14],questionnair:6,quick:[7,9],radiofield:3,rais:[6,13],randint:10,random:[6,10],raw:7,read:6,real:0,redirect:10,refer:6,region:0,regist:8,register_blueprint:8,registerform:9,registr:9,reimplement:6,relationship:7,rememb:9,render:1,report:11,repres:5,represent:7,requir:10,research:6,rest:6,result:[6,11],reward:9,rif:10,right:13,rout:[1,2,8,10,12],run:[0,6],same:[6,7,13],sampl:6,sandbox:0,satisfi:6,save:[5,6,7,11],scale:6,score:[6,7,11],scoregener:6,script:1,search:1,second:10,secret:[0,9],secret_kei:0,see:10,selectfield:9,self:9,sentiment:9,server:0,set:[0,6,9,13],show:11,signup:[11,12,14],site:[5,11],size:[6,7],some:[4,6,10],some_nam:11,sort:6,sourc:[0,1,3,4,5,6,7,8,9,10,11,13],space:9,special:9,split:6,sql:0,sqlalchemi:0,sqlalchemy_database_uri:0,sqlalchemy_track_modif:0,sqlite:0,start:14,statu:5,store:[7,10],str:[0,4,5,6,7,10,11,13],string:[7,10],stringfield:[3,9],structur:13,submit:[5,7,11],subpackag:[2,12],subrout:[4,10],subsystem:[1,8],sure:13,survei:6,system:[1,2,3,4,5,7,8,9,10,11,12,13],tabl:[7,11,13],take:7,templat:1,test:[0,4],testingconfig:0,textareafield:9,than:[6,10],thei:5,them:11,thi:[0,1,2,3,4,5,6,7,8,9,10,11,12,13],time:6,token:0,track:0,tri:10,tupl:[3,4,6,7,10],tuple_:7,tuple_id:7,tuple_s:6,tupleform:3,turk:[2,7,9,11,14],turker:[5,9],two:[2,3,6,7],txt:[6,9,11,13],type:[3,4,6,7,8,9,10,13],under:12,uniqu:[6,13],unit:[9,10],updat:6,upload:[0,6,7,9,10,11,12,13,14],upload_fil:10,upload_project:11,use:[7,10,11],used:[0,1,3,6,7,8,9,10,13],user:[1,7,8,9,10,11],user_id:7,usermixin:7,usernam:[7,9,10,11,14],uses:7,using:[0,1,3,6,7],valid:[1,3,5,8,9,11],validate_:13,validate_upload:9,validate_usernam:9,validationerror:13,valueerror:6,variabl:0,view:[1,2,12],wai:13,web:[0,7,14],welcom:1,werkzeug:10,wfgdmwpz7fx:10,when:0,where:0,whether:[0,7,9],which:[8,10],who:[3,7],whole:6,within:[5,6,11,13,14],work:6,worst:[3,6,7,9],worst_def:[7,9],worst_id:7,worst_item:3,wtf_csrf_enabl:0,wtform:13,xml:14},titles:["Configurations","Web Interface for <strong>Best-Worst-Scaling</strong>","Annotator Subsystem","Forms","Helper Functions","Routes Management","Generators","Models","Web Application","Forms","Helper Functions","Routes Management","User Subsystem","Validators","Templates"],titleterms:{"function":[4,10],account:[5,11],annot:[2,5,14],applic:8,backend:1,best:1,configur:0,content:1,form:[3,9],frontend:1,gener:6,helper:[4,10],indic:1,input:11,interfac:1,link:1,main:14,manag:[5,11],model:7,output:11,rout:[5,11],scale:1,subsystem:[2,12,14],system:14,tabl:1,templat:14,user:[12,14],valid:13,view:[5,11],web:[1,8],worst:1}})