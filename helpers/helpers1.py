

class db_tables(object):
    def __init__(self,my_self):
        self.VAnalysisSamples = None 
        self.AnalysisSamples = None 
        self.AnalysisSamples_Base = None 
        self.VAnalysis_Sections  = None 
        self.Analysis_Sections = None 
        self.Analysis_Sections_Base = None 
        self.VAnalysis_Sections_Raw = None 
        self.Analysis_Sections_Raw = None 
        self.Analysis_Sections_Raw_Base = None 
        self.VBase = None 
        self.Base = None 
        self.Base_Chunks = None 
        self.Chunks  = None 
        self.VConst_Reh_Lyr_Detail = None 
        self.Const_Reh_Lyr_Detail = None 
        self.VConst_Rehab_History = None 
        self.Const_Rehab_History = None 
        self.Const_Rehab_History_Base = None 
        self.VDist_Feat_Tenth_2012 = None 
        self.Dist_Feat_Tenth_2012 = None 
        self.Dist_Feat_Tenth_2012_Base  = None 
        self.VDstrs_Feature_2012 = None 
        self.Dstrs_Feature_2012 = None 
        self.Dstrs_Feature_2012_Base = None 
        self.VLandmark = None 
        self.Landmark = None 
        self.Landmark_Base = None 
        self.VLane = None 
        self.Lane = None 
        self.Lane_Base = None 
        self.MDOTSectionCondition = None 
        self.VProject = None 
        self.Project = None 
        self.VSRVY_DISTRESS_FEATURES = None 
        self.SRVY_DISTRESS_FEATURES = None 
        self.VSRVY_MRI_1_10_MILE = None 
        self.SRVY_MRI_1_10_MILE = None 
        self.VSRVY_PVMT_DSTRS_FEATURE_TENTH = None 
        self.SRVY_PVMT_DSTRS_FEATURE_TENTH = None 
        self.VSRVY_PVMT_SAMPLE_SGMT = None 
        self.SRVY_PVMT_SAMPLE_SGMT = None 
        self.VSRVY_PVMT_SCTN_COND = None 
        self.SRVY_PVMT_SCTN_COND = None 
        self.VSRVY_PVMT_SCTN_DISTRESS = None 
        self.SRVY_PVMT_SCTN_DISTRESS = None 
        self.VSample_Segment = None 
        self.Sample_Segment = None 
        self.Sample_Segment_Base = None 
        self.VTraffic = None 
        self.Traffic = None 
        self.Traffic_Base  = None 
        self.VWeightLimits = None 
        self.WeightLimits = None 
        self.WeightLimits_Base = None 
        self.VAnalysis_Sections_DS = None 
        self.Analysis_Sections_DS = None 
        self.Analysis_Sections_DS_Base = None 
        self.VAnalysis_Sections_DD = None 
        self.Analysis_Sections_DD = None 
        self.Analysis_Sections_DD_Base = None 
        self.MDOTDistresses = None 

def clearColorRow(table,color):
    for j in range(table.columnCount()):
        for i in range(table.rowCount()):
            table.item(i,j).setBackground(color)
    pass

def setColorRow(table,rowIndex,color):
    for j in range(table.columnCount()):
        table.item(rowIndex,j).setBackground(color)

    