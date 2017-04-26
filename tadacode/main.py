from __init__ import RAW_ENDPOINT
import data_manipulation
import data_extraction
import learning
import easysparql
import numpy as np
# To print np array without the e (scientific notation)
np.set_printoptions(suppress=True)


def main():
    class_property_combinations = [
        ('http://xmlns.com/foaf/0.1/Person', 'http://dbpedia.org/ontology/numberOfMatches'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/longew'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/latns'),
        ('http://schema.org/Place', 'http://www.georss.org/georss/point'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/latm'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/longm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latd'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longd'),
    ]
    class_property_combinations_test = [
        # ('http://schema.org/Place', 'http://dbpedia.org/property/latm'),
        # ('http://schema.org/Place', 'http://dbpedia.org/property/longm'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/latd'),
        ('http://schema.org/Place', 'http://dbpedia.org/property/longd'),
    ]

    data1, meta_data1 = data_extraction.data_and_meta_from_class_property_uris(class_property_combinations)
    data2, meta_data2 = data_extraction.data_and_meta_from_files(['novHighC.csv'])
    data, meta_data = data_manipulation.merge_data_and_meta_naive(data1=data1, meta_data1=meta_data1, data2=data2,
                                                                  meta_data2=meta_data2)
    for clus, md in enumerate(meta_data):
        print "cluster %d => type: %s" % (clus, md["type"])
    model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)

    test_data1, test_meta_data1 = data_extraction.data_and_meta_from_class_property_uris(
        class_property_combinations_test)

    test_data2, test_meta_data2 = data_extraction.data_and_meta_from_files(['mayHighC.csv'])
    # merge the two data sets
    test_data, test_meta_data = data_manipulation.merge_data_and_meta_naive(
        data1=test_data1, meta_data1=test_meta_data1, data2=test_data2, meta_data2=test_meta_data2)

    # test_meta_data_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=test_meta_data)
    # learning.test_with_data_and_meta(model=model, data=test_data, meta_data=test_meta_data_with_clusters)
    learning.predict(model=model, data=test_data, meta_data=test_meta_data)


def main_with_class_explore():
    class_uri = 'http://dbpedia.org/ontology/Person'
    properties = easysparql.get_numerical_properties_for_class_tbox(endpoint=RAW_ENDPOINT, class_uri=class_uri)
    if properties is None:
        return
    class_property_combinations = zip((len(properties) * [class_uri]), properties)
    # print class_property_combinations
    data, meta_data = data_extraction.data_and_meta_from_class_property_uris(
        class_property_uris=class_property_combinations)
    # data_extraction.save_data_and_meta_to_files(data=data, meta_data=meta_data)
    model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)
    meta_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data)
    learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_with_clusters)
    # now testing some files
    test_data, test_meta_data = data_extraction.data_and_meta_from_files(['person_waist.csv','person_hipsize.csv',
                                                          'person_bustsize.csv'])
    learning.predict(model, data=test_data, meta_data=test_meta_data)


def main_with_explore():
    classes_properties_uris = easysparql.get_all_classes_properties_numerical(RAW_ENDPOINT)
    data, meta_data = data_extraction.data_and_meta_from_class_property_uris(class_property_uris=classes_properties_uris)
    if np.any(np.isnan(data)):
        print "there is a nan in the data"
        print "**************************"
    else:
        print "no nans in the data"
    data_extraction.save_data_and_meta_to_files(data=data, meta_data=meta_data)
    model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)
    meta_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data)
    #print "model num_of_clusters: %d" % model.n_clusters
    #print "cluster centers: %s" % str(model.cluster_centers_)
    learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_with_clusters)


def main_with_local_files():
    data, meta_data = data_extraction.data_and_meta_from_files(get_local_dbpedia_files())
    model = learning.train_with_data_and_meta(data=data, meta_data=meta_data)
    meta_data_with_clusters = learning.get_cluster_for_meta(training_meta=meta_data, testing_meta=meta_data)
    learning.test_with_data_and_meta(model=model, data=data, meta_data=meta_data_with_clusters)


def get_local_dbpedia_files():
    return [
    'http_dbpedia_org_ontology_AcademicJournal_http_dbpedia_org_ontology_impactFactor',
    'http_dbpedia_org_ontology_Airport_http_dbpedia_org_ontology_runwayLength',
    'http_dbpedia_org_ontology_ArchitecturalStructure_http_dbpedia_org_ontology_visitorsPercentageChange',
    'http_dbpedia_org_ontology_Athlete_http_dbpedia_org_ontology_espnId',
    'http_dbpedia_org_ontology_AutomobileEngine_http_dbpedia_org_ontology_acceleration',
    'http_dbpedia_org_ontology_AutomobileEngine_http_dbpedia_org_ontology_co2Emission',
    'http_dbpedia_org_ontology_AutomobileEngine_http_dbpedia_org_ontology_cylinderBore',
    'http_dbpedia_org_ontology_AutomobileEngine_http_dbpedia_org_ontology_displacement',
    'http_dbpedia_org_ontology_AutomobileEngine_http_dbpedia_org_ontology_pistonStroke',
    'http_dbpedia_org_ontology_AutomobileEngine_http_dbpedia_org_ontology_powerOutput',
    'http_dbpedia_org_ontology_AutomobileEngine_http_dbpedia_org_ontology_torqueOutput',
    'http_dbpedia_org_ontology_Automobile_http_dbpedia_org_ontology_fuelCapacity',
    'http_dbpedia_org_ontology_Automobile_http_dbpedia_org_ontology_wheelbase',
    'http_dbpedia_org_ontology_BaseballPlayer_http_dbpedia_org_ontology_statisticValue',
    'http_dbpedia_org_ontology_Biomolecule_http_dbpedia_org_ontology_omim',
    'http_dbpedia_org_ontology_BodyOfWater_http_dbpedia_org_ontology_shoreLength',
    'http_dbpedia_org_ontology_Bridge_http_dbpedia_org_ontology_loadLimit',
    'http_dbpedia_org_ontology_Bridge_http_dbpedia_org_ontology_mainspan',
    'http_dbpedia_org_ontology_Broadcaster_http_dbpedia_org_ontology_effectiveRadiatedPower',
    'http_dbpedia_org_ontology_Broadcaster_http_dbpedia_org_ontology_heightAboveAverageTerrain',
    'http_dbpedia_org_ontology_Broadcaster_http_dbpedia_org_ontology_shareOfAudience',
    'http_dbpedia_org_ontology_Building_http_dbpedia_org_ontology_floorArea',
    'http_dbpedia_org_ontology_Canal_http_dbpedia_org_ontology_maximumBoatBeam',
    'http_dbpedia_org_ontology_Canal_http_dbpedia_org_ontology_maximumBoatLength',
    'http_dbpedia_org_ontology_Canal_http_dbpedia_org_ontology_originalMaximumBoatBeam',
    'http_dbpedia_org_ontology_Canal_http_dbpedia_org_ontology_originalMaximumBoatLength',
    'http_dbpedia_org_ontology_CareerStation_http_dbpedia_org_ontology_numberOfGoals',
    'http_dbpedia_org_ontology_CareerStation_http_dbpedia_org_ontology_numberOfMatches',
    'http_dbpedia_org_ontology_CelestialBody_http_dbpedia_org_ontology_absoluteMagnitude',
    'http_dbpedia_org_ontology_CelestialBody_http_dbpedia_org_ontology_apoapsis',
    'http_dbpedia_org_ontology_CelestialBody_http_dbpedia_org_ontology_periapsis',
    'http_dbpedia_org_ontology_Colour_http_dbpedia_org_ontology_cmykCoordinateBlack',
    'http_dbpedia_org_ontology_Colour_http_dbpedia_org_ontology_cmykCoordinateCyanic',
    'http_dbpedia_org_ontology_Colour_http_dbpedia_org_ontology_cmykCoordinateMagenta',
    'http_dbpedia_org_ontology_Colour_http_dbpedia_org_ontology_cmykCoordinateYellow',
    'http_dbpedia_org_ontology_Colour_http_dbpedia_org_ontology_hsvCoordinateHue',
    'http_dbpedia_org_ontology_Colour_http_dbpedia_org_ontology_hsvCoordinateSaturation',
    'http_dbpedia_org_ontology_Colour_http_dbpedia_org_ontology_hsvCoordinateValue',
    'http_dbpedia_org_ontology_Colour_http_dbpedia_org_ontology_wavelength',
    'http_dbpedia_org_ontology_Drug_http_dbpedia_org_ontology_bioavailability',
    'http_dbpedia_org_ontology_Event_http_dbpedia_org_ontology_duration',
    'http_dbpedia_org_ontology_Food_http_dbpedia_org_ontology_approximateCalories',
    'http_dbpedia_org_ontology_Food_http_dbpedia_org_ontology_carbohydrate',
    'http_dbpedia_org_ontology_Food_http_dbpedia_org_ontology_fat',
    'http_dbpedia_org_ontology_Food_http_dbpedia_org_ontology_glycemicIndex',
    'http_dbpedia_org_ontology_Food_http_dbpedia_org_ontology_maxTime',
    'http_dbpedia_org_ontology_Food_http_dbpedia_org_ontology_minTime',
    'http_dbpedia_org_ontology_Food_http_dbpedia_org_ontology_protein',
    'http_dbpedia_org_ontology_Food_http_dbpedia_org_ontology_servingSize',
    'http_dbpedia_org_ontology_GeneLocation_http_dbpedia_org_ontology_geneLocationEnd',
    'http_dbpedia_org_ontology_GeneLocation_http_dbpedia_org_ontology_geneLocationStart',
    'http_dbpedia_org_ontology_GeneLocation_http_dbpedia_org_ontology_onChromosome',
    'http_dbpedia_org_ontology_GrandPrix_http_dbpedia_org_ontology_course',
    'http_dbpedia_org_ontology_Island_http_dbpedia_org_ontology_governmentElevation',
    'http_dbpedia_org_ontology_Lake_http_dbpedia_org_ontology_areaOfCatchment',
    'http_dbpedia_org_ontology_Person_http_dbpedia_org_ontology_bustSize',
    'http_dbpedia_org_ontology_Person_http_dbpedia_org_ontology_hipSize',
    'http_dbpedia_org_ontology_Person_http_dbpedia_org_ontology_waistSize',
    'http_dbpedia_org_ontology_Place_http_dbpedia_org_ontology_areaLand',
    'http_dbpedia_org_ontology_Place_http_dbpedia_org_ontology_areaTotal',
    'http_dbpedia_org_ontology_Place_http_dbpedia_org_ontology_areaWater',
    'http_dbpedia_org_ontology_Place_http_dbpedia_org_ontology_averageDepth',
    'http_dbpedia_org_ontology_Place_http_dbpedia_org_ontology_depth',
    'http_dbpedia_org_ontology_Place_http_dbpedia_org_ontology_elevation',
    'http_dbpedia_org_ontology_Place_http_dbpedia_org_ontology_maximumDepth',
    'http_dbpedia_org_ontology_Place_http_dbpedia_org_ontology_maximumElevation',
    'http_dbpedia_org_ontology_Place_http_dbpedia_org_ontology_minimumElevation',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_albedo',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_apparentMagnitude',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_escapeVelocity',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_maximumTemperature',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_meanRadius',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_meanTemperature',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_minimumTemperature',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_orbitalPeriod',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_rotationPeriod',
    'http_dbpedia_org_ontology_Planet_http_dbpedia_org_ontology_surfaceArea',
    'http_dbpedia_org_ontology_PopulatedPlace_http_dbpedia_org_ontology_areaRural',
    'http_dbpedia_org_ontology_PopulatedPlace_http_dbpedia_org_ontology_areaUrban',
    'http_dbpedia_org_ontology_PopulatedPlace_http_dbpedia_org_ontology_populationDensity',
    'http_dbpedia_org_ontology_PopulatedPlace_http_dbpedia_org_ontology_populationMetroDensity',
    'http_dbpedia_org_ontology_PopulatedPlace_http_dbpedia_org_ontology_populationUrbanDensity',
    'http_dbpedia_org_ontology_PowerStation_http_dbpedia_org_ontology_averageAnnualGeneration',
    'http_dbpedia_org_ontology_PowerStation_http_dbpedia_org_ontology_capacityFactor',
    'http_dbpedia_org_ontology_PowerStation_http_dbpedia_org_ontology_installedCapacity',
    'http_dbpedia_org_ontology_RadioStation_http_dbpedia_org_ontology_facilityId',
    'http_dbpedia_org_ontology_Rocket_http_dbpedia_org_ontology_lowerEarthOrbitPayload',
    'http_dbpedia_org_ontology_RouteOfTransportation_http_dbpedia_org_ontology_lineLength',
    'http_dbpedia_org_ontology_RouteOfTransportation_http_dbpedia_org_ontology_railGauge',
    'http_dbpedia_org_ontology_RouteOfTransportation_http_dbpedia_org_ontology_speedLimit',
    'http_dbpedia_org_ontology_RouteOfTransportation_http_dbpedia_org_ontology_trackLength',
    'http_dbpedia_org_ontology_RouteOfTransportation_http_dbpedia_org_ontology_voltageOfElectrification',
    'http_dbpedia_org_ontology_School_http_dbpedia_org_ontology_averageClassSize',
    'http_dbpedia_org_ontology_School_http_dbpedia_org_ontology_barPassRate',
    'http_dbpedia_org_ontology_School_http_dbpedia_org_ontology_campusSize',
    'http_dbpedia_org_ontology_School_http_dbpedia_org_ontology_testaverage',
    'http_dbpedia_org_ontology_Settlement_http_dbpedia_org_ontology_distanceToBelfast',
    'http_dbpedia_org_ontology_Settlement_http_dbpedia_org_ontology_distanceToCardiff',
    'http_dbpedia_org_ontology_Settlement_http_dbpedia_org_ontology_distanceToCharingCross',
    'http_dbpedia_org_ontology_Settlement_http_dbpedia_org_ontology_distanceToDouglas',
    'http_dbpedia_org_ontology_Settlement_http_dbpedia_org_ontology_distanceToDublin',
    'http_dbpedia_org_ontology_Settlement_http_dbpedia_org_ontology_distanceToEdinburgh',
    'http_dbpedia_org_ontology_Settlement_http_dbpedia_org_ontology_distanceToLondon',
    'http_dbpedia_org_ontology_Ship_http_dbpedia_org_ontology_shipBeam',
    'http_dbpedia_org_ontology_Ship_http_dbpedia_org_ontology_shipDisplacement',
    'http_dbpedia_org_ontology_Ship_http_dbpedia_org_ontology_shipDraft',
    'http_dbpedia_org_ontology_SnookerPlayer_http_dbpedia_org_ontology_centuryBreaks',
    'http_dbpedia_org_ontology_SnookerPlayer_http_dbpedia_org_ontology_currentRank',
    'http_dbpedia_org_ontology_SnookerPlayer_http_dbpedia_org_ontology_highestBreak',
    'http_dbpedia_org_ontology_SnookerPlayer_http_dbpedia_org_ontology_highestRank',
    'http_dbpedia_org_ontology_Station_http_dbpedia_org_ontology_numberOfPlatformLevels',
    'http_dbpedia_org_ontology_Stream_http_dbpedia_org_ontology_discharge',
    'http_dbpedia_org_ontology_Stream_http_dbpedia_org_ontology_watershed',
    'http_dbpedia_org_ontology_TelevisionShow_http_dbpedia_org_ontology_tvComId',
    'http_dbpedia_org_ontology_University_http_dbpedia_org_ontology_other',
    'http_dbpedia_org_ontology_Work_http_dbpedia_org_ontology_runtime'
    ]











# main()
# main_with_class_explore()
main_with_explore()
# main_with_local_files()


