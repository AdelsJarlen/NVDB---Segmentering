"""
Eksempel på bruk av segmenteringsrutine: 
    Vegnett + trafikkmengde + fartsgrense for Oslo kommune
"""
from datetime import datetime 
import pandas
import geopandas 
from shapely import wkt

import STARTHER
import nvdbapiv3
from nvdbapiv3 import segmentering


if __name__ == '__main__': 
    t0 = datetime.now()

    # # Henter vegnett for hele Oslo!
    # vegnett = pandas.DataFrame( nvdbapiv3.nvdbVegnett( 
    #     filter={
    #         'fylke' : 3, 
    #         'veglenketype' : 'hoved,konnektering',
    #     }).to_records() )
    # # vegreferanse    = pandas.DataFrame( nvdbapiv3.nvdbVegnett(objTypeID = 532, filter = {'fylke' : 3}).to_records())
    
    # fartsgrense     = pandas.DataFrame( nvdbapiv3.nvdbFagdata(objTypeID = 105, filter = {'fylke' : 3}).to_records())
    # trafikkmengde   = pandas.DataFrame( nvdbapiv3.nvdbFagdata(objTypeID = 540, filter = { 'fylke' : 3 }).to_records())
    # vegbredde       = pandas.DataFrame( nvdbapiv3.nvdbFagdata(objTypeID = 838, filter = {'fylke':3}).to_records())
    # feltstrekning   = pandas.DataFrame( nvdbapiv3.nvdbFagdata(objTypeID = 616, filter = {'fylke':3}).to_records())

    # Konvertert geosjon av Bydel Sagene fra Overpass Turbo
    polygon_string = "-1188648.286011767 61.617106873155436,-1188648.2858821715 61.61708836554098,-1188648.2845021593 61.61709689598111,-1188648.2841052974 61.61710645708031,-1188648.2806110694 61.61720320026802,-1188648.2803831378 61.61719990950938,-1188648.2796802965 61.61720946983785,-1188648.2789011677 61.617214917243494,-1188648.2787243705 61.61722581553446,-1188648.2785219022 61.617235171486755,-1188648.2762829552 61.617286574980646,-1188648.2760902164 61.61730775505811,-1188648.2742592068 61.61744161982944,-1188648.274277733 61.61834354171237,-1188648.2743283466 61.61943033091981,-1188648.2734293498 61.620484524344626,-1188648.2730380767 61.62096468466489,-1188648.2719973756 61.620714422382036,-1188648.271242572 61.62052924478227,-1188648.27091734 61.62044153998148,-1188648.2701888285 61.620191381303336,-1188648.2695516143 61.619931660756365,-1188648.2686150458 61.619512776778386,-1188648.2683225235 61.61937633620156,-1188648.266463982 61.61856869403469,-1188648.2662409153 61.6186782977452,-1188648.2654526755 61.61910622538592,-1188648.265048878 61.61934938956965,-1188648.2648338845 61.61946937794537,-1188648.264683897 61.619563456281654,-1188648.2646123709 61.619602424224574,-1188648.2644821538 61.619657431669296,-1188648.2643061841 61.61975150994009,-1188648.2641629246 61.619787084699546,-1188648.2640131437 61.61984219491321,-1188648.2638330334 61.619896688140905,-1188648.2636293238 61.619933393748994,-1188648.2634139173 61.619961668229756,-1188648.2631016236 61.61999755101819,-1188648.262177475 61.620062118561826,-1188648.2616892129 61.620104170003,-1188648.2608169238 61.62024328092064,-1188648.2606606213 61.620272378096416,-1188648.260497798 61.620324300910966,-1188648.2602778368 61.62037498976239,-1188648.259469103 61.620609310555096,-1188648.259169645 61.62072929871802,-1188648.2588047679 61.62088475901821,-1188648.2576584828 61.62148778526504,-1188648.256446779 61.622113431365676,-1188648.2561146112 61.622233316627934,-1188648.2560296278 61.62248624934997,-1188648.2558596611 61.62287233151329,-1188648.2554680766 61.62347248074964,-1188648.2551160345 61.623900615125386,-1188648.2549137727 61.62410810187809,-1188648.254587608 61.624405554302,-1188648.254254094 61.62461766754605,-1188648.253827938 61.624875945958465,-1188648.2533459894 61.62514337505604,-1188648.2521785893 61.625707741581074,-1188648.2520976432 61.62575154195876,-1188648.2522354156 61.62597897631177,-1188648.253305095 61.62823450332306,-1188648.253622043 61.62924037522467,-1188648.2538555628 61.62993326811228,-1188648.256181448 61.63468676807853,-1188648.2565290371 61.63536033141955,-1188648.256678818 61.635341001962786,-1188648.2570099484 61.635977036594966,-1188648.2570685362 61.63597066201005,-1188648.2572503008 61.63636651279489,-1188648.2577059572 61.6363018412532,-1188648.2581599562 61.636579760172054,-1188648.2588508928 61.63691248182406,-1188648.259117745 61.637022806496645,-1188648.2594692681 61.637146292120676,-1188648.2601914662 61.6373510051094,-1188648.2613437525 61.63757535747078,-1188648.2620661566 61.63764702362291,-1188648.2623200694 61.63766655973334,-1188648.2627561616 61.63768630193936,-1188648.2630363668 61.63768311527912,-1188648.26370712 61.63762831483304,-1188648.2648597178 61.637430803846755,-1188648.2657258997 61.63726238970831,-1188648.2666243776 61.63710055602031,-1188648.2675856866 61.63691569119882,-1188648.2690144521 61.63666975350466,-1188648.26954826 61.6365855466892,-1188648.2696331395 61.63640715721021,-1188648.2699345646 61.63643666681226,-1188648.2702464447 61.63571992146041,-1188648.2702679767 61.63540817652983,-1188648.2701749206 61.6350559209134,-1188648.2704032664 61.6350319648326,-1188648.2706049066 61.63501901023902,-1188648.2708003358 61.63503535883584,-1188648.2711517562 61.63507772084716,-1188648.2712236969 61.63499649459768,-1188648.271644366 61.63512800022076,-1188648.2726032927 61.635331171531995,-1188648.2730523243 61.63537353378928,-1188648.2733910135 61.63536705709182,-1188648.2736320905 61.63534125031427,-1188648.273866441 61.63528932767999,-1188648.2740006952 61.635232675153276,-1188648.2742927005 61.63508739367802,-1188648.2745429906 61.63493162463445,-1188648.2747068487 61.63481276713091,-1188648.2748178132 61.634773902105664,-1188648.2750258707 61.63475446997745,-1188648.2752016326 61.63475447042028,-1188648.2752175727 61.63510035110992,-1188648.2751681972 61.635344955642196,-1188648.277610232 61.63589997479928,-1188648.280163546 61.63482666134534,-1188648.2806322444 61.634713356796226,-1188648.2841550435 61.63396135286849,-1188648.284708725 61.63378964775788,-1188648.2849690563 61.63373453782279,-1188648.2855550337 61.633595117729314,-1188648.2859196006 61.63352047258613,-1188648.2864536156 61.633403775198694,-1188648.2866811324 61.63364714660954,-1188648.2868440582 61.63385165255278,-1188648.2873841797 61.633851551095354,-1188648.2875016655 61.63352726257775,-1188648.2875535258 61.633321626174705,-1188648.2875607726 61.63314436750095,-1188648.2875154347 61.63288814426574,-1188648.2873270446 61.63250853874994,-1188648.2867744009 61.63169411386592,-1188648.285656588 61.630104335007886,-1188648.2856128025 61.630017761916896,-1188648.285533409 61.629864254044506,-1188648.285539828 61.62930718469097,-1188648.2856320594 61.628501603802675,-1188648.285691684 61.62764523060842,-1188648.285708143 61.62734160830795,-1188648.2857967503 61.626662288242166,-1188648.2857968544 61.62653253158968,-1188648.2858949855 61.625505274532955,-1188648.2859152744 61.62495900113237,-1188648.2859873208 61.624109105520176,-1188648.286006988 61.62388516738454,-1188648.286072512 61.623518517610094,-1188648.2860855546 61.623336940583705,-1188648.286124786 61.62306755682343,-1188648.2861375196 61.62261669875542,-1188648.2861933124 61.62228439025754,-1188648.2862860593 61.62204451547464,-1188648.2864530229 61.621813688886185,-1188648.2865360396 61.62165617151052,-1188648.2866012524 61.62149073708345,-1188648.286694102 61.621213950543,-1188648.286824011 61.62066017168505,-1188648.286868935 61.62034852963141,-1188648.2868614823 61.620226381511635,-1188648.2868628295 61.61975794149131,-1188648.2868065205 61.619488043399016,-1188648.2866402827 61.61880512405193,-1188648.2861043052 61.61734685122332,-1188648.286011767 61.617106873155436, -1188648.286011767 61.617106873155436,-1188648.286011767 61.617106873155436"
    
    # Firkanten polygon fra mindre område i Oslo
    polygon_string_2 = "-1188648.2890588397 61.632714223031535,-1188648.2890588683 61.62129208803966,-1188648.267989771 61.6212920349667,-1188648.2679897428 61.63271416994873,-1188648.2890588397 61.632714223031535"

    wkt_polygon_string = "POLYGON ((-1188648.2890588397 61.632714223031535,-1188648.2890588683 61.62129208803966,-1188648.267989771 61.6212920349667,-1188648.2679897428 61.63271416994873,-1188648.2890588397 61.632714223031535))"

    # Henter vegnett for polygon_string_2.
    vegnett = pandas.DataFrame( nvdbapiv3.nvdbVegnett( 
        filter={
            'srid' : 5973,
            'polygon' : wkt_polygon_string,
            'veglenketype' : 'hoved,konnektering',
        }).to_records() )
    fartsgrense     = pandas.DataFrame( nvdbapiv3.nvdbFagdata(objTypeID = 105, filter = {'polygon':polygon_string_2}).to_records())
    trafikkmengde   = pandas.DataFrame( nvdbapiv3.nvdbFagdata(objTypeID = 540, filter = {'polygon':polygon_string_2}).to_records())
    vegbredde       = pandas.DataFrame( nvdbapiv3.nvdbFagdata(objTypeID = 838, filter = {'polygon':polygon_string_2}).to_records())
    feltstrekning   = pandas.DataFrame( nvdbapiv3.nvdbFagdata(objTypeID = 616, filter = {'polygon':polygon_string_2}).to_records())

    # Lager GeodataFrame   
    vegnett         = geopandas.GeoDataFrame( vegnett,       geometry =  vegnett['geometri'].apply( wkt.loads), crs=5973 )
    fartsgrense     = geopandas.GeoDataFrame( fartsgrense,   geometry =  fartsgrense['geometri'].apply( wkt.loads), crs=5973 )
    trafikkmengde   = geopandas.GeoDataFrame( trafikkmengde, geometry =  trafikkmengde['geometri'].apply( wkt.loads), crs=5973 )
    vegbredde       = geopandas.GeoDataFrame( vegbredde,     geometry =  vegbredde['geometri'].apply( wkt.loads), crs=5973 )
    feltstrekning   = geopandas.GeoDataFrame( feltstrekning, geometry =  feltstrekning['geometri'].apply( wkt.loads), crs=5973 )

    print( f"Tidsbruk datanedlasting: {datetime.now()-t0}")
    # Legger på gatenavn
    vegnett['gatenavn'] = vegnett['gate'].apply( lambda x : x['navn'] if isinstance( x, dict) else '' )

    # Tar kun med disse kolonnene fra vegnettet:
    vegnett_col = ['gatenavn', 'veglenkesekvensid', 'startposisjon', 'sluttposisjon',
        'type', 'detaljnivå', 'typeVeg', 
        'feltoversikt', 'geometri', 'lengde', 'fylke',
       'kommune',  'vref',
       'vegkategori', 'fase', 'nummer',
        'trafikantgruppe', 'adskilte_lop', 'medium', 'geometry' ]
    
    # Og kun disse kolonnene fra fartsgrense:  
    fart_col = ['objekttype', 'Fartsgrense', 'veglenkesekvensid',
       'vref',  'startposisjon', 'sluttposisjon',
       'segmentlengde', 'geometry']
    
    # Og kun disse fra trafikkmengde: 
    traf_col = ['objekttype', 'År, gjelder for',
       'ÅDT, total', 'ÅDT, andel lange kjøretøy', 'Grunnlag for ÅDT',
       'veglenkesekvensid', 'vref', 
       'startposisjon', 'sluttposisjon', 'geometry']
    
    # Kolonner fra vegbredde
    vegb_col = ['objekttype','Dekkebredde', 'veglenkesekvensid', 'vref','startposisjon','sluttposisjon','geometry']

    # Kolonner fra feltstrekning
    felts_col = ['objekttype',5528,'veglenkesekvensid','vref','startposisjon','sluttposisjon','geometry']
    
    t1 = datetime.now()
    segmentert = segmentering.segmenter( vegnett[vegnett_col], [ fartsgrense[fart_col], trafikkmengde[traf_col], vegbredde[vegb_col], feltstrekning[felts_col] ])
    print( f"Tidsbruk segmentering: {datetime.now()-t1}")

    filnavn =  'oslo_segmentertveg_' + str( datetime.now() )[0:10] + '.gpkg'


    segmentert.to_file( filnavn )

    # vil du heller ha Esri fil-geodatabase? (.GDB, også kalt FGDB)
    # filnavn =  'oslo_segmentertveg_' + str( datetime.now() )[0:10] + '.gdb'
    # segmentert.to_file( filnavn,  driver= 'OpenFileGDB' )
    # 
    # Eventuelt gi ditt eget navn på vegnettet
    # segmentert.to_file( filnavn, layer='vegnett', driver= 'OpenFileGDB' )

##############################################################
###
### Resultat fra kjøring på Jans PC 
###
# In [28]: %run script_segmenteringseksempel_Oslo.py
# Eksport av 97643 vegsegmenter kommer til å ta tid...
# Vegsegment 1000 av 97643
# Vegsegment 5000 av 97643
# Vegsegment 10000 av 97643
# Vegsegment 20000 av 97643
# Vegsegment 30000 av 97643
# Vegsegment 40000 av 97643
# Vegsegment 50000 av 97643
# Vegsegment 60000 av 97643
# Vegsegment 70000 av 97643
# Vegsegment 80000 av 97643
# Vegsegment 90000 av 97643
# Eksport av 44529 objekter kommer til å ta tid...
# Objekt 1000 av 44530
# Objekt 5000 av 44530
# Objekt 10000 av 44530
# Objekt 20000 av 44530
# Objekt 30000 av 44530
# Objekt 40000 av 44530
# Manglende geometri-element for 1 vegobjekter fra dette søket
# nvdbFagdata: Søkeobjekt for vegobjekter fra NVDB api V3
# ObjektType: 105 Fartsgrense
# Filtere
# {
#     "fylke": 3
# }
# Parametre som styrer responsen:
# {
#     "inkluder": [
#         "alle"
#     ]
# }
# Statistikk fra NVDB api V3
# {
#     "antall": 44529,
#     "lengde": 3786696.135
# }
# Pagineringsinfo: Antall objekt i databuffer= 0
# {
#     "antall": 1000,
#     "hvilken": 1,
#     "antallObjektReturnert": 44530,
#     "meredata": false,
#     "initielt": false,
#     "dummy": false
# }
# fra miljø https://nvdbapiles-v3.atlas.vegvesen.no/
# Objekt 1000 av 7180
# Objekt 5000 av 7180
# Tidsbruk datanedlasting: 0:01:25.670870
# Segmentering av 97643 datarader med veg og 2 typer fagdata med ialt 61202 datarader
# Segmentering: Behandler vegsegment 1 av 97643 ( 0% ) tidsbruk 0:00:00
# Segmentering: Behandler vegsegment 10 av 97643 ( 0% ) tidsbruk 0:00:00
# Segmentering: Behandler vegsegment 100 av 97643 ( 0% ) tidsbruk 0:00:01
# Segmentering: Behandler vegsegment 500 av 97643 ( 1% ) tidsbruk 0:00:07
# Segmentering: Behandler vegsegment 1000 av 97643 ( 1% ) Estimert ferdig om: 0:23:11 

# Degenert tilfelle (f.eks stedfesting MOT?) veglenkesekvens=603948 kommune=301
#         Vegnett=(0.472888,0.56167774), fagdata=(0.54244942, 0.56167774) 
#         kv11635 s1d1 m787-815 
#         POINT (265316.278 6648583.083) - POINT (265404.801 6648809.232)

# Segmentering: Behandler vegsegment 10000 av 97643 ( 10% ) Estimert ferdig om: 0:21:03 
# Segmentering: Behandler vegsegment 20000 av 97643 ( 20% ) Estimert ferdig om: 0:18:31 
# Segmentering: Behandler vegsegment 30000 av 97643 ( 31% ) Estimert ferdig om: 0:16:06 
# Segmentering: Behandler vegsegment 40000 av 97643 ( 41% ) Estimert ferdig om: 0:13:25 
# Segmentering: Behandler vegsegment 50000 av 97643 ( 51% ) Estimert ferdig om: 0:10:59 
# Segmentering: Behandler vegsegment 60000 av 97643 ( 61% ) Estimert ferdig om: 0:08:40 
# Segmentering: Behandler vegsegment 70000 av 97643 ( 72% ) Estimert ferdig om: 0:06:19 
# Segmentering: Behandler vegsegment 80000 av 97643 ( 82% ) Estimert ferdig om: 0:04:01 
# Segmentering: Behandler vegsegment 90000 av 97643 ( 92% ) Estimert ferdig om: 0:01:44 
# Segmentering ferdig, tidsbruk: 0:22:10
# Tidsbruk segmentering: 0:22:11.486519