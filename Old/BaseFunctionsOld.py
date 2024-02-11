# Assignment:   Extra Credit 1
#
# Program Name: as_extraCredit_01.py
#
# Purpose:
#
#
#
#
# Author:       Alex Somheil
# Course:       192CIS115.600
#
# Created:      Written on 4/20/2019

import re


postDELFunGuide = {0:"-",1:"Richardson",2:"Turner",3:"Young",4:"Bynum",5:"Young",6:"Hawes",7:"Wright",8:"Allen",9:"Moultrie",10:"Wilkins",11:"Ivey",12:"Brown",13:"Jenkins",14:"Walker",15:"Henderson",16:"Kidd-Gilchrist",17:"Mullens",18:"Biyombo",19:"Sessions",20:"Gordon",21:"Adrien",22:"Haywood",23:"McRoberts",24:"Pargo",25:"Taylor",26:"Williams",27:"Thomas",28:"Diop",29:"Jennings",30:"Ellis",31:"Mbah a Moute",32:"Ilyasova",33:"Sanders",34:"Henson",35:"Dunleavy",36:"Udoh",37:"Redick",38:"Daniels",39:"Ayon",40:"Smith",41:"Dalembert",42:"Gooden",43:"Przybilla",44:"Rose",45:"Butler",46:"Deng",47:"Boozer",48:"Noah",49:"Hinrich",50:"Gibson",51:"Belinelli",52:"Robinson",53:"Hamilton",54:"Teague",55:"Cook",56:"Mohammed",57:"Radmanovic",58:"Irving",59:"Waiters",60:"Gee",61:"Thompson",62:"Varejao",63:"Ellington",64:"Miles",65:"Speights",66:"Gibson",67:"Zeller",68:"Livingston",69:"Casspi",70:"Walton",71:"Quinn",72:"Rondo",73:"Bradley",74:"Pierce",75:"Bass",76:"Garnett",77:"Terry",78:"Green",79:"Sullinger",80:"Lee",81:"Crawford",82:"Wilcox",83:"Williams",84:"White",85:"Melo",86:"Paul",87:"Billups",88:"Butler",89:"Griffin",90:"Jordan",91:"Crawford",92:"Barnes",93:"Odom",94:"Bledsoe",95:"Turiaf",96:"Green",97:"Hill",98:"Hollins",99:"Wayns",100:"Summers",101:"Conley",102:"Allen",103:"Prince",104:"Randolph",105:"Gasol",106:"Pondexter",107:"Bayless",108:"Arthur",109:"Dooling",110:"Daye",111:"Davis",112:"Wroten",113:"Leuer",114:"Greene",115:"Teague",116:"Williams",117:"Korver",118:"Smith",119:"Horford",120:"Harris",121:"Pachulia",122:"Johnson",123:"Stevenson",124:"Jenkins",125:"Petro",126:"Mack",127:"Tolliver",128:"Jones",129:"Scott",130:"Chalmers",131:"Wade",132:"James",133:"Haslem",134:"Bosh",135:"Allen",136:"Battier",137:"Cole",138:"Andersen",139:"Miller",140:"Anthony",141:"Lewis",142:"Jones",143:"Howard",144:"Vasquez",145:"Gordon",146:"Aminu",147:"Davis",148:"Lopez",149:"Anderson",150:"Rivers",151:"Thomas",152:"Smith",153:"Roberts",154:"Henry",155:"Amundson",156:"Mason",157:"Miller",158:"Williams",159:"Foye",160:"Hayward",161:"Millsap",162:"Jefferson",163:"Favors",164:"Burks",165:"Williams",166:"Tinsley",167:"Kanter",168:"Carroll",169:"Watson",170:"Evans",171:"Thomas",172:"Evans",173:"Salmons",174:"Thompson",175:"Cousins",176:"Thornton",177:"Patterson",178:"Hayes",179:"Douglas",180:"Fredette",181:"Outlaw",182:"Aldrich",183:"Johnson",184:"Felton",185:"Prigioni",186:"Shumpert",187:"Anthony",188:"Chandler",189:"Smith",190:"Stoudemire",191:"Kidd",192:"Martin",193:"Novak",194:"Copeland",195:"Richardson",196:"White",197:"Barron",198:"Camby",199:"Nash",200:"Bryant",201:"World Peace",202:"Gasol",203:"Howard",204:"Blake",205:"Hill",206:"Jamison",207:"Meeks",208:"Clark",209:"Goudelock",210:"Morris",211:"Duhon",212:"Sacre",213:"Ebanks",214:"Nelson",215:"Afflalo",216:"Harris",217:"Davis",218:"Vucevic",219:"Harkless",220:"Nicholson",221:"Udrih",222:"O'Quinn",223:"Jones",224:"Moore",225:"Lamb",226:"Harrington",227:"Turkoglu",228:"James",229:"Mayo",230:"Marion",231:"Nowitzki",232:"Kaman",233:"Carter",234:"Collison",235:"Wright",236:"Brand",237:"Crowder",238:"Beaubois",239:"Morrow",240:"James",241:"Cunningham",242:"Williams",243:"Johnson",244:"Wallace",245:"Evans",246:"Lopez",247:"Watson",248:"Blatche",249:"Humphries",250:"Bogans",251:"Teletovic",252:"Brooks",253:"Joseph",254:"Taylor",255:"Shengelia",256:"Stackhouse",257:"Lawson",258:"Iguodala",259:"Gallinari",260:"Faried",261:"McGee",262:"Koufos",263:"Chandler",264:"Miller",265:"Brewer",266:"Randolph",267:"Fournier",268:"Mozgov",269:"Hamilton",270:"Miller",271:"Hill",272:"George",273:"Granger",274:"West",275:"Hibbert",276:"Hansbrough",277:"Pendergraph",278:"Augustin",279:"Stephenson",280:"Green",281:"Johnson",282:"Mahinmi",283:"Plumlee",284:"Young",285:"Calderon",286:"Knight",287:"Singler",288:"Maxiell",289:"Monroe",290:"Drummond",291:"Stuckey",292:"Jerebko",293:"Bynum",294:"Villanueva",295:"English",296:"Middleton",297:"Kravtsov",298:"Maggette",299:"Lowry",300:"DeRozan",301:"Gay",302:"Bargnani",303:"Valanciunas",304:"Johnson",305:"Anderson",306:"Fields",307:"Telfair",308:"Ross",309:"Gray",310:"Lucas",311:"Pietrus",312:"Acy",313:"Kleiza",314:"Lin",315:"Harden",316:"Parsons",317:"Smith",318:"Asik",319:"Delfino",320:"Beverley",321:"Robinson",322:"Motiejunas",323:"Garcia",324:"Jones",325:"Brooks",326:"Anderson",327:"White",328:"Parker",329:"Green",330:"Leonard",331:"Duncan",332:"Splitter",333:"Ginobili",334:"Diaw",335:"Neal",336:"Bonner",337:"Joseph",338:"Blair",339:"De Colo",340:"Mills",341:"McGrady",342:"Dragic",343:"Johnson",344:"Tucker",345:"Scola",346:"Gortat",347:"Dudley",348:"Frye",349:"Beasley",350:"Morris",351:"Marshall",352:"Brown",353:"Morris",354:"O'Neal",355:"Haddadi",356:"Westbrook",357:"Sefolosha",358:"Durant",359:"Ibaka",360:"Perkins",361:"Martin",362:"Collison",363:"Jackson",364:"Thabeet",365:"Fisher",366:"Brewer",367:"Jones",368:"Liggins",369:"Lamb",370:"Orton",371:"Rubio",372:"Ridnour",373:"Kirilenko",374:"Love",375:"Pekovic",376:"Budinger",377:"Barea",378:"Stiemsma",379:"Shved",380:"Williams",381:"Lee",382:"Cunningham",383:"Lillard",384:"Matthews",385:"Batum",386:"Aldridge",387:"Hickson",388:"Leonard",389:"Barton",390:"Freeland",391:"Maynor",392:"Claver",393:"Babbitt",394:"Pavlovic",395:"Williams",396:"Smith",397:"Curry",398:"Thompson",399:"Barnes",400:"Lee",401:"Bogut",402:"Jack",403:"Landry",404:"Rush",405:"Ezeli",406:"Green",407:"Jefferson",408:"Bazemore",409:"Biedrins",410:"Wall",411:"Beal",412:"Ariza",413:"Nenê",414:"Okafor",415:"Webster",416:"Seraphin",417:"Booker",418:"Temple",419:"Price",420:"Vesely",421:"Martin",422:"Collins",423:"Singleton",424:"Barbosa",425:"Johnson",426:"Jordan",427:"Bird",428:"Barkley",429:"Robinson",430:"Pippen",431:"Ewing",432:"Malone",433:"Mullin",434:"Drexler",435:"Stockton",436:"Laettner",437:"Paul",438:"Bryant",439:"Durant",440:"James",441:"Chandler",442:"Williams",443:"Anthony",444:"Love",445:"Westbrook",446:"Harden",447:"Iguodala",448:"Davis",449:"Jones",450:"Jones",451:"Havlicek",452:"Sanders",453:"Russell",454:"Heinsohn",455:"Siegfried",456:"Thompson",457:"Counts",458:"Smith",459:"Williams",460:"Jones",461:"West",462:"Barnett",463:"Baylor",464:"Larusso",465:"Ellis",466:"King",467:"Imhoff",468:"Nelson",469:"Davis",470:"Brown",471:"Johnson",472:"Smith",473:"Robertson",474:"McGlocklin",475:"Dandridge",476:"Smith",477:"Cunningham",478:"Allen",479:"Davis",480:"Brown",481:"Miller",482:"Smith",483:"Williams",484:"Jones",485:"West",486:"Goodrich",487:"Erickson",488:"Baylor",489:"Chamberlain",490:"McMillian",491:"McCarter",492:"Roberson",493:"Davis",494:"Brown",495:"Johnson",496:"Miller",497:"Maravich",498:"Hudson",499:"Chambers",500:"Bridges",501:"Bellamy",502:"Davis",503:"Chappell",504:"Smith",505:"Williams",506:"Jones",507:"Davis",508:"Johnson",509:"West",510:"Goodrich",511:"McMillian",512:"Ellis",513:"Chamberlain",514:"Robinson",515:"Erickson",516:"Baylor",517:"Brown",518:"Johnson",519:"Miller",520:"Smith",521:"Frazier",522:"Barnett",523:"Bradley",524:"DeBusschere",525:"Lucas",526:"Jackson",527:"Monroe",528:"Reed",529:"Rackley",530:"Williams",531:"Jones",532:"Davis",533:"Bibby",534:"Collins",535:"Bryant",536:"McGinnis",537:"Dawkins",538:"Free",539:"Mix",540:"Catchings",541:"Dunleavy",542:"Miller",543:"Smith",544:"Johnson",545:"Cheeks",546:"Richardson",547:"Jones",548:"Johnson",549:"Malone",550:"Johnson",551:"Miller",552:"Brown",553:"Johnson",554:"Smith",555:"Williams",556:"Davis",557:"Hodges",558:"Moncrief",559:"Pressey",560:"Cummings",561:"Lister",562:"Dunleavy",563:"Pierce",564:"Mokeski",565:"Breuer",566:"Davis",567:"Jones",568:"Davis",569:"Macy",570:"Jordan",571:"Gervin",572:"Green",573:"Oakley",574:"Corzine",575:"Paxson",576:"Higgins",577:"Brown",578:"Johnson",579:"Miller",580:"Williams",581:"Johnson",582:"Ainge",583:"Bird",584:"McHale",585:"Parish",586:"Walton",587:"Sichting",588:"Wedman",589:"Vincent",590:"Smith",591:"Williams",592:"Jones",593:"Rivers",594:"Wittman",595:"Wilkins",596:"Willis",597:"Rollins",598:"Levingston",599:"Johnson",600:"Koncak",601:"Webb",602:"Carr",603:"Hastings",604:"Davis",605:"Johnson",606:"Scott",607:"Worthy",608:"Green",609:"Thompson",610:"Cooper",611:"Rambis",612:"Thompson",613:"Brickowski",614:"Brown",615:"Johnson",616:"Davis",617:"Paxson",618:"Jordan",619:"Pippen",620:"Grant",621:"Cartwright",622:"Vincent",623:"Sellers",624:"Hodges",625:"Corzine",626:"Davis",627:"Perdue",628:"Miller",629:"Thomas",630:"Dumars",631:"Aguirre",632:"Mahorn",633:"Laimbeer",634:"Rodman",635:"Johnson",636:"Edwards",637:"Salley",638:"Dawkins",639:"Smith",640:"Williams",641:"Price",642:"Ehlo",643:"Nance",644:"Williams",645:"Daugherty",646:"Kerr",647:"Williams",648:"Rollins",649:"Mokeski",650:"Jones",651:"Davis",652:"Brown",653:"Paxson",654:"Jordan",655:"Pippen",656:"Grant",657:"Cartwright",658:"Armstrong",659:"Perdue",660:"Levingston",661:"Hodges",662:"Williams",663:"Johnson",664:"Davis",665:"Johnson",666:"Scott",667:"Worthy",668:"Perkins",669:"Divac",670:"Green",671:"Drew",672:"Thompson",673:"Campbell",674:"Miller",675:"Smith",676:"Williams",677:"Porter",678:"Drexler",679:"Kersey",680:"Williams",681:"Duckworth",682:"Robinson",683:"Ainge",684:"Bryant",685:"Petrovic",686:"Jones",687:"Davis",688:"Brown",689:"Hardaway",690:"Richmond",691:"Mullin",692:"Hill",693:"Lister",694:"Higgins",695:"Marciulionis",696:"Tolbert",697:"Elie",698:"Mokeski",699:"Askew",700:"Johnson",701:"Armstrong",702:"Jordan",703:"Pippen",704:"Grant",705:"Cartwright",706:"Williams",707:"Paxson",708:"McCray",709:"Perdue",710:"Nealy",711:"Smith",712:"Davis",713:"Bogues",714:"Gill",715:"Wingate",716:"Johnson",717:"Mourning",718:"Curry",719:"Newman",720:"Gattison",721:"Bennett",722:"Green",723:"Lynch",724:"Williams",725:"Smith",726:"Maxwell",727:"Horry",728:"Thorpe",729:"Olajuwon",730:"Elie",731:"Cassell",732:"Brooks",733:"Bullard",734:"Jones",735:"Davis",736:"Brown",737:"Abdul-Rauf",738:"Stith",739:"Williams",740:"Ellis",741:"Mutombo",742:"Pack",743:"Rogers",744:"Hammonds",745:"Johnson",746:"Miller",747:"Smith",748:"Williams",749:"Harper",750:"Starks",751:"Smith",752:"Oakley",753:"Ewing",754:"Mason",755:"Davis",756:"Bonner",757:"Anthony",758:"Williams",759:"Williams",760:"Christie",761:"Hardaway",762:"Anderson",763:"Royal",764:"Grant",765:"O'Neal",766:"Scott",767:"Shaw",768:"Bowie",769:"Turner",770:"Rollins",771:"Davis",772:"Brown",773:"Harper",774:"Jordan",775:"Pippen",776:"Rodman",777:"Longley",778:"Kukoc",779:"Kerr",780:"Wennington",781:"Simpkins",782:"Buechler",783:"Salley",784:"Edwards",785:"Payton",786:"Hawkins",787:"Schrempf",788:"Kemp",789:"Johnson",790:"Perkins",791:"Askew",792:"McMillan",793:"Brickowski",794:"Wingate",795:"Johnson",796:"Miller",797:"Harper",798:"Jordan",799:"Pippen",800:"Rodman",801:"Longley",802:"Kukoc",803:"Kerr",804:"Wennington",805:"Buechler",806:"Simpkins",807:"Smith",808:"Williams",809:"Stockton",810:"Hornacek",811:"Keefe",812:"Malone",813:"Foster",814:"Ostertag",815:"Anderson",816:"Eisley",817:"Carr",818:"Jones",819:"Davis",820:"Williams",821:"Fisher",822:"Bryant",823:"Jones",824:"Horry",825:"O'Neal",826:"Campbell",827:"Blount",828:"Barry",829:"Brown",830:"Johnson",831:"Miller",832:"Smith",833:"Johnson",834:"Del Negro",835:"Elliott",836:"Duncan",837:"Robinson",838:"Jackson",839:"Person",840:"Perdue",841:"Williams",842:"Williams",843:"Jones",844:"Davis",845:"McKie",846:"Iverson",847:"Lynch",848:"Hill",849:"Mutombo",850:"Jones",851:"Geiger",852:"MacCulloch",853:"Bell",854:"Miller",855:"Smith",856:"Brown",857:"Bibby",858:"Christie",859:"Stojakovic",860:"Pollard",861:"Divac",862:"Jackson",863:"Turkoglu",864:"Wallace",865:"Funderburke",866:"Brown",867:"Johnson",868:"Miller",869:"Wang",870:"Peete",871:"Timmerman",872:"Schroeder",873:"Boenisch",874:"Anderson",875:"Jones",876:"Harris",877:"Burchanowski",878:"Townsend",879:"Townsend",880:"Park",881:"Boucher",882:"Darroca",883:"Bow Wow",884:"Pauly D",885:"Bieber",886:"Smoove",887:"Kingston",888:"Guadagnino",889:"Wale",890:"Williams",891:"Mill",892:"Miller",893:"Baumgartner",894:"Wale",895:"Bieber",896:"Smoove",897:"Kingston",898:"Bow Wow",899:"Pauly D",900:"Guadagnino",901:"Williams",902:"Mill",903:"Miller",904:"Baumgartner",905:"Braun",906:"Good",907:"Flores",908:"Hamilton",909:"Chamillionaire",910:"Taylor",911:"Perez",912:"Miller",913:"Harrison",914:"Lincoln",915:"Lincoln",916:"Messi",917:"Kambavolo",918:"Humpdus",919:"W Bush",920:"Gandhi",921:"Mosley",922:"Laatz",923:"Gandhi",924:"Nigga",925:"Kid",926:"Steifbold",927:"Kid",928:"Sanchevaste",929:"Carlin",930:"Nigga",931:"Obama",932:"Messi",933:"Gha-Die",934:"Jeeves",935:"Kambavolo",936:"Sadman",937:"Bro",938:"Christ",939:"Somheil",940:"Kowalczyk",941:"Clark",942:"Miller",943:"Steifbold",944:"Slave",945:"Mosley",946:"Clark",947:"Laatz",948:"Harrison",949:"Kowalczyk",950:"Somheil",951:"Rogers",952:"Peanut",953:"Buffett",954:"Hennesey",955:"Ho",956:"Mckez",957:"Kid",958:"Kid",959:"Kid",960:"Kid",961:"Kid",962:"Kid",963:"Kid",964:"Kid",965:"Kid",966:"Kid",967:"Kid",968:"Kid",969:"Kid",970:"Kid",971:"Shearcliff",972:"Shearcliff",973:"Shearcliff",974:"Shearcliff",975:"Shearcliff",976:"Shearcliff",977:"Shearcliff",978:"Shearcliff",979:"Shearcliff",980:"Shearcliff",981:"Shearcliff",982:"Shearcliff",983:"Shearcliff",984:"Shearcliff",985:"Bleakstar",986:"****************",987:"****************",988:"****************",989:"****************",990:"****************",991:"****************",992:"****************",993:"****************",994:"****************",995:"****************",996:"****************",997:"****************",998:"****************",999:"****************",1000:"****************",1001:"****************",1002:"****************",1003:"****************",1004:"****************",1005:"****************",1006:"****************",1007:"****************",1008:"****************",1009:"****************",1010:"****************",1011:"****************",1012:"****************",1013:"****************",1014:"****************",1015:"****************",1016:"****************",1017:"****************",1018:"****************",1019:"****************",1020:"****************",1021:"****************",1022:"****************",1023:"****************",1024:"****************",1025:"****************",1026:"****************",1027:"****************",1028:"****************",1029:"****************",1030:"****************",1031:"****************",1032:"****************",1033:"****************",1034:"****************",1035:"****************",1036:"****************",1037:"****************",1038:"****************",1039:"****************",1040:"****************",1041:"****************",1042:"****************",1043:"****************",1044:"****************",1045:"****************",1046:"****************",1047:"****************",1048:"****************",1049:"****************",1050:"****************",1051:"****************",1052:"****************",1053:"****************",1054:"****************",1055:"****************",1056:"****************",1057:"****************",1058:"****************",1059:"****************",1060:"****************",1061:"****************",1062:"****************",1063:"****************",1064:"****************",1065:"****************",1066:"****************",1067:"****************",1068:"****************",1069:"****************",1070:"****************",1071:"****************",1072:"****************",1073:"****************",1074:"****************",1075:"****************",1076:"****************",1077:"Harrison",1078:"Miller",1079:"Steifbold",1080:"Clark",1081:"Rogers",1082:"Mckez",1083:"McSludge",1084:"Gandhitron",1085:"Sanchevaste",1086:"Kid",1087:"Lincoln",1088:"Bro",1089:"the Thief",1090:"Laatz",1091:"McBasketball",1092:"Somheil",1093:"Kowalczyk",1094:"Gandhi",1095:"Judas",1096:"Ruiz",1097:"Messi",1098:"Kambavolo",1099:"Humpdus",1100:"Hennesey",1101:"Bratton",1102:"Broccoli",1103:"Pickles",1104:"McDippledugel",1105:"Fletcher",1106:"Jeeves",1107:"Buffett",1108:"Beelzebub",1109:"Sadman",1110:"Gha-Die",1111:"Rizzy",1112:"Slave",1113:"Host",1114:"Obama",1115:"Stukas",1116:"Warrior",1117:"Kirkwood",1118:"Gumbo",1119:"Squarepants",1120:"Brutus",1121:"Morty",1122:"Goodman",1123:"Kripparrian",1124:"Mophead",1125:"Tickletits",1126:"Harper",1127:"Sloan",1128:"Trump",1129:"Benningham",1130:"Sheep",1131:"Pickles",1132:"White",1133:"White Jr",1134:"Squid",1135:"Star",1136:"Tentacles",1137:"Kawinaka",1138:"Malvo",1139:"Alderson",1140:"Phil",1141:"Robot",1142:"Nye",1143:"Freeman",1144:"Nigga",1145:"Jalapeno",1146:"Leaf",1147:"McPips",1148:"Claus",1149:"Yoda",1150:"Abawabagru",1151:"Mehta",1152:"Benlodan",1153:"Papertowel",1154:"Pelzer",1155:"Milkdud",1156:"San Roman",1157:"Elmo",1158:"Crab",1159:"Ethan",1160:"White",1161:"Krabs",1162:"Lowly Janitor",1163:"Vsauce",1164:"-",1165:"Nara",1166:"Charles",1167:"Pickles",1168:"Kertez",1169:"Scalliwag",1170:"Sneh",1171:"Linus",1172:"Strawberry",1173:"Pete",1174:"Sanchevaste",1175:"Ehrmantraut",1176:"Fishlips",1177:"Cornbread",1178:"Exile",1179:"Locke",1180:"Chicken",1181:"Bob Crawfish",1182:"Snow",1183:"Hudson",1184:"Lesterson Lee",1185:"McDonald",1186:"Lannister",1187:"Man",1188:"Philosopher",1189:"Critikal",1190:"Bleakstar",1191:"Dick",1192:"Hound",1193:"Morgan",1194:"Millerando",1195:"Kilgrave",1196:"Hodor",1197:"Senior Slave",1198:"Judes",1199:"Jay",1200:"Tron",1201:"Morozov",1202:"Thor",1203:"Giantsbane",1204:"Viridius",1205:"Bain",1206:"Kid",1207:"Littlenose",1208:"H'Ghar",1209:"Antagonist",1210:"Pickles",1211:"Thinker",1212:"Davos",1213:"King",1214:"Rick",1215:"Mountain",1216:"van der Linde",1217:"Chissano",1218:"Lannister",1219:"Bildgerat",1220:"Titticaca",1221:"Innkeeper",1222:"Rick",1223:"Bot",1224:"Littlefinger",1225:"Testificate",1226:"Customer",1227:"Albot",1228:"Schrader",1229:"Bounty Hunter",1230:"Maximus",1231:"Shadow",1232:"Narrator",1233:"Mormont",1234:"Pickles",1235:"Littlenose",1236:"Agent",1237:"Vulcano",1238:"Tank",1239:"Mar Chiquita",1240:"Pree",1241:"Nigh",1242:"Cool",1243:"Nigga",1244:"Osborne",1245:"King Jr",1246:"Ritman",1247:"Kolento",1248:"Dishwasher",1249:"The Nite",1250:"Holmes",1251:"Warrens",1252:"Nygaard",1253:"Testicles",1254:"Tarth",1255:"Shearcliff",1256:"Moriarty",1257:"Club",1258:"Molkosky",1259:"Chissano",1260:"DisRespect",1261:"Fieri",1262:"Nigga",1263:"Commander",1264:"Devil",1265:"Drogo",1266:"O'Houlihan",1267:"Tarly",1268:"Dishwasher",1269:"Greyjoy",1270:"Velocity",1271:"Shearcliff",1272:"Protagonist",1273:"Pradagucci",1274:"Baratheon",1275:"Carl",1276:"Piber",1277:"****************",1278:"****************",1279:"****************",1280:"****************",1281:"****************",1282:"****************",1283:"****************",1284:"****************",1285:"****************",1286:"****************",1287:"****************",1288:"****************",1289:"****************",1290:"****************",1291:"****************",1292:"****************",1293:"****************",1294:"****************",1295:"****************",1296:"****************",1297:"****************",1298:"****************",1299:"****************",1300:"****************",1301:"****************",1302:"****************",1303:"****************",1304:"****************",1305:"****************",1306:"****************",1307:"****************",1308:"****************",1309:"****************",1310:"****************",1311:"****************",1312:"****************",1313:"****************",1314:"****************",1315:"****************",1316:"****************",1317:"****************",1318:"****************",1319:"****************",1320:"****************",1321:"****************",1322:"****************",1323:"****************",1324:"****************",1325:"****************",1326:"****************",1327:"****************",1328:"****************",1329:"****************",1330:"****************",1331:"Alabi",1332:"Allen",1333:"Azubuike",1334:"Battie",1335:"Bell",1336:"Bibby",1337:"Brockman",1338:"Butler",1339:"Cardinal",1340:"Carney",1341:"Carroll",1342:"Childress",1343:"Collins",1344:"Cook",1345:"Daniels",1346:"Douglas-Roberts",1347:"Dupree",1348:"Elson",1349:"Ely",1350:"Evans",1351:"Eyenga",1352:"Fesenko",1353:"Gadzuric",1354:"Gladness",1355:"Greene",1356:"Harangody",1357:"Harper",1358:"Harrellson",1359:"Hayward",1360:"Higgins",1361:"Hobson",1362:"Honeycutt",1363:"Jackson",1364:"Jackson",1365:"James",1366:"Jeffries",1367:"Johnson",1368:"Johnson",1369:"Johnson-Odom",1370:"Jones",1371:"Jones",1372:"Leslie",1373:"Mbenga",1374:"McGuire",1375:"Moon",1376:"Morrison",1377:"Murphy",1378:"Pargo",1379:"Pittman",1380:"Price",1381:"Posey",1382:"Rautins",1383:"Redd",1384:"Ross",1385:"Samuels",1386:"Selby",1387:"Simmons",1388:"Skinner",1389:"Sloan",1390:"Thomas",1391:"Thompkins",1392:"Tyler",1393:"Uzoh",1394:"Walker",1395:"Warrick",1396:"Weaver",1397:"West",1398:"Whiteside",1399:"Williams",1400:"Williams",1401:"Wright",1402:"Zeller",1403:"Satoransky",1404:"Hamilton",1405:"Murphy",1406:"Papanikolaou",1407:"Turkyilmaz",1408:"Kuzmic",1409:"Aldemir",1410:"Zubcic",1411:"Karaman",1412:"Hummel",1413:"Denmon",1414:"Williams",1415:"Johnson",1416:"Owens",1417:"Davis",1418:"Harris",1419:"Johnson",1420:"Thompson",1421:"Stone",1422:"Wright",1423:"Jordan",1424:"Reid",1425:"Thomas",1426:"Ager",1427:"Ajinca",1428:"Alexander",1429:"Andersen",1430:"Arenas",1431:"Armstrong",1432:"Arroyo",1433:"Balkman",1434:"Banks",1435:"Bell",1436:"Boykins",1437:"Brackins",1438:"Brown",1439:"Caracter",1440:"Carter",1441:"Collins",1442:"Curry",1443:"Dampier",1444:"Davis",1445:"Diogu",1446:"Dorsey",1447:"Dowdell",1448:"Erden",1449:"Ewing Jr",1450:"Farmar",1451:"Fernandez",1452:"Flynn",1453:"Forbes",1454:"Ford",1455:"Foster",1456:"Gaines",1457:"Gomes",1458:"Graham",1459:"Graham",1460:"Harris",1461:"Harris",1462:"Head",1463:"House",1464:"Howard",1465:"Hudson",1466:"Janning",1467:"Jeter",1468:"Johnson",1469:"Kapono",1470:"Krstic",1471:"Law",1472:"Lawal",1473:"Macklin",1474:"Magloire",1475:"Marks",1476:"McDyess",1477:"Mensah-Bonsu",1478:"Milicic",1479:"Miller",1480:"Najera",1481:"N'diaye",1482:"Nocioni",1483:"Oden",1484:"Okur",1485:"Parker",1486:"Peterson",1487:"Powe",1488:"Powell",1489:"Ratliff",1490:"Roy",1491:"Scalabrine",1492:"Shakur",1493:"Siler",1494:"Smith",1495:"Smith",1496:"Stojakovic",1497:"Songaila",1498:"Sy",1499:"Taylor",1500:"Thomas",1501:"Thornton",1502:"Udoka",1503:"Vaden",1504:"Vujacic",1505:"Wafer",1506:"Wallace",1507:"Wallace",1508:"Warren",1509:"Weems",1510:"West",1511:"White",1512:"Williams",1513:"Williams",1514:"Wright"}


# Function figures out what the type of a string is by reading the first
# character (if it is a [, it's a list, { is a dict, etc) then converts it into
# the identified type.
def convertToTypeSimple(string):
    trimString = string.lstrip()
    first = trimString[0]
    # Tests if it is a string starting with '
    if first == "'":
        string0 = string.lstrip()
        string1 = string0.lstrip("'")
        string2 = string1.rstrip("'")
        result = string2

    # Tests if it is a string starting with "
    elif first == '"':
        string0 = string.lstrip()
        string1 = string0.lstrip('"')
        string2 = string1.rstrip('"')
        result = string2


    # Tests if it is a list starting with [
    elif first == '[':
        result = stringToList(string)

    # Tests if it is a dicitonary starting with {
    elif first == '{':
        result = stringToDict(string)


    # If none of these are true, 3 possibilities remain. 1. The string is
    # a string, but it isn't denoted by quotations or apostrophes. If the
    # program finds any letters in the string at this point, it will just be
    # converted into a string. 2. If the string has no letters but contains a
    # period, it is assumed to be a float. 3. If nothing else works, the string
    # must be an integer.
    else:
        letterTest = re.search('[a-zA-Z]', string)
        if letterTest == None:
            if '.' in string:
                result = float(string)
            else:
                result = int(string)
        else:
            result = str(string)
    return result


# Function converts a string into a list.
def stringToList(string):
    string0 = string.strip()
    string1 = string0.lstrip('[')
    string2 = string1.rstrip(']')
    newList = []
    value = ''
    openBracketCount = 0
    for x in string2:

        # Quick check to make sure openBracketCount didn't go negative
        if openBracketCount < 0:
            openBracketCount = 0

        # 'Safe Mode' for cases where there is a list or dictionary within a
        # list.
        if openBracketCount != 0:
            if x in '[{':
                openBracketCount += 1
            elif x in ']}':
                openBracketCount += -1
            value += x
            continue

        # This checks to see if there is another list or dictionary INSIDE this
        # list. If there is, it goes into 'safe mode' and just blindly
        # concatenates all characters without prejudice until the ending )} is
        # found.
        if x in '[{':
            value += x
            openBracketCount += 1
            continue


        # This checks if the value is a comma, signaling the next item in the
        # list. When true, the program will append the previous value and clear
        # the value variable for further use.
        elif x == ',':
            finalValue = convertToTypeSimple(value)
            newList.append(finalValue)
            value = ''

        # When none of these other conditions are true, it simply concatenates
        # x to the value.
        else:
            value += x

    # For lists, we have to append the final value to the list because no comma
    # will follow it. Otherwise, function would skip the final value.
    finalValue = convertToTypeSimple(value)
    newList.append(finalValue)
    value = ''
    return newList


# Function converts a string into a dictionary.
def stringToDict(string):
    string0 = string.strip()
    string1 = string0.lstrip('{')
    string2 = string1.rstrip('}')
    newDict = {}
    value = ''
    key = ''
    entry = ''
    skip = 0
    openBracketCount = 0
    for x in string2:

        # Quick check to make sure openBracketCount didn't go negative
        if openBracketCount < 0:
            openBracketCount = 0

        # 'Safe Mode' for cases where there is a list or dictionary within a
        # list.
        if openBracketCount != 0:
            if x in '[{':
                openBracketCount += 1
            elif x in ']}':
                openBracketCount += -1
            value += x
            continue

        # This checks if the character after the colon is a space (like it is
        # supposed to be.) If it is, it just skips it, if it isn't, it treats
        # it normally
        if skip == 1:
            skip = 0
            if x == ' ':
                continue

        # This checks to see if there is another list or dictionary INSIDE this
        # dictionary. If there is, it goes into 'safe mode' and just blindly
        # concatenates all characters without prejudice until the ending )} is
        # found.
        if x in '{[':
            value += x
            openBracketCount += 1
            continue

        # This checks if the character is a colon, signaling the switch between
        # the key and the entry. If true, the 'key' variable is set to the value
        # for later use, and nullifies the value. It also sets up the skip
        # sentinel to check whether or not a space character follows the colon.
        elif x == ':':
            key = convertToTypeSimple(value)
            value = ''
            skip = 1
            continue





        # This checks if the character is a comma, signaling the end of a dict
        # entry. If this is true, it converts the value to its type and then
        # adds the dictionary entry using the previously gotten key value and
        # the now got entry value.
        elif x == ',':
            entry = convertToTypeSimple(value)
            newDict[key] = entry
            key = ''
            entry = ''
            value = ''


        # If none of these cases are true, then x is just concatenated to value.
        else:
            value += x

    # For dictionaries, we have to append the remaining value when the for loop
    # ends as an entry, because no commas will follow and the last key/entry
    # would otherwise be skipped.
    entry = convertToTypeSimple(value)
    newDict[key] = entry
    key = ''
    entry = ''
    value = ''
    return newDict


# This function returns a string starting at the given index, and removes
# everything before that.
def getStringAt(string, index):
    counter = -1
    value = ''
    for x in string:
        counter += 1
        if index <= counter:
            value += x
    return value


# Given a character or list of characters, this function counts how many times
# they collectively appear in a string.
def countFreq(characters, string):
    charList = str(characters)
    counter = 0
    for x in charList:
        for y in string:
            if x == y:
                counter += 1
    return counter


# Function returns the index of the highest entry in a list of numbers. Function
# ignores any entry that isn't a number. Function prioritizes finding earlier
# numbers on the list.
def getMaxIndex(list1):
    counter = 0
    index = 0
    for x in list1:
        try:
            test = float(x)
            if test > list1[index]:
                index = counter
            counter += 1
        except:
            counter += 1
            continue
    return index


# Same as previous function, but returns the index of the lowest entry in a list
# of numbers. Again, skips non-number entries. Function prioritizes finding
# later numbers on the list over earlier numbers, unlike getMaxIndex.
def getMinIndex(list1):
    counter = 0
    for x in list1:
        try:
            test = float(x)
            if counter == 0:
                index = counter
            if test <= list1[index]:
                index = counter
            counter += 1
            continue
        except:
            counter += 1
            continue
    return index




# This function reads a config value from a config file, with a custom format.
def readConfigValue(parameterName):
    configFile = open("../config.txt", "r")
    foundParameter = False
    arrayOfValues = []
    for i in configFile:
        if (i[0] == ">"):
            if (parameterName in str(i)):
                foundParameter = True
                if("=" in str(i)):
                    item = ""
                    foundEqualSign = False
                    for j in i:
                        if(foundEqualSign == False):
                            if(j == "="):
                                foundEqualSign = True
                        else:
                            item += j
                    returnValue = item.lstrip(" \n\t")
                    returnValue = returnValue.rstrip(" \n\t")
                    configFile.close()
                    return returnValue


        if (foundParameter == True):
            if (i == ";\n"):
                break
            elif (i == "\n"):
                continue
            else:
                item = ""
                thisValue = []
                for j in i:
                    if(j == ","):
                        thisValue.append(item)
                        item = ""
                    else:
                        if(j == "\n"):
                            continue
                        item += j
                if(item != ""):
                    thisValue.append(item)
                arrayOfValues.append(thisValue)
    configFile.close()
    return arrayOfValues