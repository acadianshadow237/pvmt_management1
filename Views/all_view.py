import sys
import operator

from PySide6.QtWidgets import (QApplication, QWidget, QPushButton, QLabel, QLineEdit, QGridLayout, QMessageBox, QComboBox, QDialog)
from PySide6 import QtCore
from PySide6 import QtGui

from helpers.helpers1 import clearColorRow, setColorRow

from Views.VCRHVCRLDVPROJ_view_ui import Ui_VCRHVCRLDVPROJ_Form
from Views.VCRH_view_ui import Ui_VCRH_Form
from Views.VCRH_Edit_ui import Ui_VCRH_Edit_Form
from Views.VProj_Edit_ui import  Ui_VProj_Edit_Form
from Views.VAS_view_ui import Ui_VAS_Form
from Views.VCRLD_Edit_ui import Ui_VCRLD_Edit_Form
from Views.RouteProjectEntry_ui import Ui_rtProjEntryForm

from Controllers.orm_select import county_select, route_select, direction_select, VAS_select
from Models.login_model import login_stuff
from Models.tableModel import MyTableModel , tableCreate2
import sqlalchemy as sa



class VAS_view(Ui_VAS_Form):
    def __init__(self,my_self):
        super(VAS_view, self).__init__()
           
        #self.fileName = 'VAS'
        self.index = 0
        self.my_login = login_stuff()
        self.my_db_tables = my_self.my_db_tables
        self.my_url = my_self.my_url
        self.database_type = my_self.my_login.database_type
        self.my_session = my_self.my_session
        self.my_login = my_self.my_login
        self.setWindowFlag

        self.my_VAS_Sql = None
        self.my_VAS_DS_Sql = None
        self.my_VAS_DD_Sql = None
        self.my_VAS_Theaders = None
        self.my_VAS_DS_Theaders = None
        self.my_VAS_DD_Theaders = None

        self.my_county = None
        self.my_route = None
        self.my_sri = None
        self.my_from = None
        self.my_to = None

        self.setupUi(self)

        self.setup_county()        

       
        self.comboBoxCounty.currentIndexChanged.connect(self.county_change)
        self.comboBoxRoute.currentIndexChanged.connect(self.route_change)
        self.comboBoxDirection.currentIndexChanged.connect(self.direction_change)
        self.VAS_tableWidget.cellClicked.connect(self.selectRow)
        self.VAS_DS_tableWidget.cellClicked.connect(self.selectRow)
        self.VAS_DD_tableWidget.cellClicked.connect(self.selectRow)

        self.pushButtonReset.clicked.connect(self.reset_all)
        self.tabWidget.setCurrentIndex(0)
        self.VAS_tab.setFocus()
    
    def county_change(self):
        if self.comboBoxCounty.currentIndex == 0:
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.setCurrentIndex(0)
            self.FilterColumncheckBox.setChecked(False)
        else:
            self.FilterColumncheckBox.setChecked(True)
            self.comboBoxRoute.clear()
            self.comboBoxDirection.clear()
            self.setup_route()
            
        pass

    def route_change(self):
        if self.comboBoxRoute.currentIndex == 0:
            
            self.comboBoxDirection.clear()
            pass
        else:
            self.setup_direction()

    def direction_change(self):
        if self.comboBoxDirection.currentIndex == 0  :
           
            
            pass
        else:
            my_direction = self.comboBoxDirection.currentText()
            if my_direction.strip() == '':
                pass
            else:
                self.my_sri = my_direction[:my_direction.find(' ')]
                self.my_from = my_direction[my_direction.find(': ')+1 : my_direction.find('T') ]
                self.my_from = float(self.my_from.strip())
                self.my_to = my_direction[my_direction.find('To: ')+3:]
                self.my_to = float(self.my_to.strip())
               
                self.fill_tables()
            
                      

        pass
    
    def reset_all(self):
        self.comboBoxCounty.setCurrentIndex(0)
        self.comboBoxRoute.setCurrentIndex(0)
        self.comboBoxDirection.setCurrentIndex(0)
        self.VAS_tableWidget.clearContents()
        self.VAS_DS_tableWidget.clearContents()
        self.VAS_DS_tableWidget.clearContents()
        self.FilterColumncheckBox.setChecked(False)
       

    def setup_county(self):
        c1 = county_select(self)
        self.comboBoxCounty.addItems(c1.get_county())

    def setup_route(self):
        if self.comboBoxCounty.currentIndex == 0:
            
            self.comboBoxDirection.clear()
            pass
        else:
            rt1 = route_select(self)
            my_temp_list = rt1.get_route()
     
            for item in my_temp_list:
                self.comboBoxRoute.addItem(str(item))     
            self.setup_direction()
            pass       

    def setup_direction(self):
        my_list = []
        if self.comboBoxDirection.currentIndex == 0 :
            
            pass
        else:
            if self.comboBoxRoute.currentIndex != 0:
                db = self.my_db_tables.VBase
                tm_county = self.comboBoxCounty.currentText()
                tm_county = tm_county[tm_county.find('[')+1:tm_county.find(']')]
                tm_route = self.comboBoxRoute.currentText()
                stmt = sa.select(db.c.Name,db.c.From,db.c.To).filter(db.c.County == tm_county).filter(db.c.Route_ID == tm_route).order_by(db.c.Name,db.c.From)
                results = self.my_session.execute(stmt)
            
                my_list.clear()
                my_list.insert(0,'')
                for item in results:
                    if item is None:
                        pass
                    else:
                        my_str = item[0] + ' From: ' + str(item[1]) + ' To: ' + str(item[2])
                        my_list.append(my_str)

            self.comboBoxDirection.clear()        
            self.comboBoxDirection.addItems(my_list) 


    def fill_tables(self):

        if  self.my_VAS_Sql == None:
            self.my_VAS_Sql = None
            self.my_VAS_DS_Sql = None
            self.my_VAS_DD_Sql = None
            self.my_VAS_Theaders = None
            self.my_VAS_DS_Theaders = None
            self.my_VAS_DD_Theaders = None

            my_item = ''  
            my_keys = [] 
            my_data = []
            my_temp = []
            my_vas = []
            my_ds = []
            my_dd = []
  
            my_vas_keys = '''
ID,Name,RoadName,From,To,pvmt_analysis_section_id,Pavement_A,
FilterColumn,maint_dis_nmbr,FunctionClass,dd_avg_fault_depth_qty,
dd_avg_iri_qty,dd_avg_rut_depth,dd_distress_rating_nmbr,dd_faults_qty,
dd_pvmt_condition_rating_nmbr,dd_pvmt_section_survey_year,dd_roughness_rating_nmbr,data_accum_direction,
dd_data_orientation,pvmt_condition_rating_nmbr,pvmt_type_code,pvmt_type_desc	,
left_shoulder_width_code,left_shoulder_width_desc,right_shoulder_width_code,right_shoulder_width_desc,
road_type,route_id,pvmt_structure_nmbr,pvmt_type_code_clustering,
section_lane_cnt,section_total_lanes,survey_avg_lane_width,total_roadway_width_code,
total_roadway_width_desc,county_name,county_nmbr,create_date,
create_user,update_date,update_user,divided_hwy_ind,
Budget_Category_Override,com_cost,com_treat,com_year,
Comments,EOLD,ESAL,RD_Name,RT_Class,Reversed,SRI,SRI_From,SRI_To,
Segment,Segment_Length,Trt_Family,Year,anl_chip_seal,anl_rural,anlss_sctn_annual_flex_esal,
anlss_sctn_annual_rigid_esal,anlss_sctn_cumul_flex_esal,anlss_sctn_cumul_rigid_esal,begin_english_station_nmbr,
begin_landmark_desc,begin_lat,begin_long,dFragWithSkip_Cluster,design_lane_width,document_id,
end_english_station_nmbr,end_landmark_desc,end_lat,end_long,esal_aadt,esal_flexible_annual,
esal_kip_factor,esal_pct_trucks,esal_rigid_annual,full_annual_flexible_esal,full_annual_rigid_esal,
full_cumulative_flexible_esal,full_cumulative_rigid_esal,max_design_hourly_vol,max_design_hourly_vol_year,
max_trffc_growth_rate,max_trffc_section_aadt,max_trffc_section_aadt_year,max_truck_trffc_pct,
measured_section_length,paved_shoulder_ind,ph_pvmt_proj_actl_end_date,ph_pvmt_rehab_affctd_srfc_pct,
ph_rehab_thickness,ph_rehab_type_code,ph_resurfacing_type_code,plan_section_length,pvmt_analysis_section_id_ ,
pvmt_anlyss_sctn_nhs_ind,pvmt_mdfd_structure_nmbr,pvmt_memo,pvmt_pre_type_code,traffic_esal_base_year,weight'''

            my_ds_keys = '''ID,Name,RoadName,From,To,pvmt_analysis_section_id,ds_Alligator_Cracking_0,ds_Alligator_Cracking_1,ds_Alligator_Cracking_2,ds_Bleeding_0,ds_Bleeding_1,ds_Bleeding_2,ds_Block_Cracking_0	,ds_Block_Cracking_1
,ds_Block_Cracking_2	,ds_Blowup_0	,ds_Blowup_1	,ds_Blowup_2	,ds_Corner_Break_0,ds_Corner_Break_1	,ds_Corner_Break_2	,ds_D_Cracking_0	,ds_D_Cracking_1	,ds_D_Cracking_2
,ds_Edge_Cracking_0	,ds_Edge_Cracking_1	,ds_Edge_Cracking_2	,ds_Faulting_0,ds_Faulting_1	,ds_Faulting_2	,ds_IRI_0	,ds_IRI_1	,ds_IRI_2	,ds_Joint_Count_0,ds_Joint_Count_1	,ds_Joint_Count_2	,ds_Joint_Deterioration_0	,ds_Joint_Deterioration_1
,ds_Joint_Deterioration_2	,ds_Joint_Seal_Deterioration_0	,ds_Joint_Seal_Deterioration_1,ds_Joint_Seal_Deterioration_2	,ds_Lane_Shoulder_Dropoff_0	,ds_Lane_Shoulder_Dropoff_1,ds_Lane_Shoulder_Dropoff_2	,ds_Longitudinal_Cracking_0	,ds_Longitudinal_Cracking_1
,ds_Longitudinal_Cracking_2	,ds_Map_Cracking_0	,ds_Map_Cracking_1	,ds_Map_Cracking_2,ds_Patching_0	,ds_Patching_1	,ds_Patching_2	,ds_Potholes_0	,ds_Potholes_1,ds_Potholes_2	,ds_Pumping_0	,ds_Pumping_1	,ds_Pumping_2	,ds_Punchouts_0
,ds_Punchouts_1	,ds_Punchouts_2	,ds_Raveling_0	,ds_Raveling_1	,ds_Raveling_2,ds_Refl_Crack_Transverse_0	,ds_Refl_Crack_Transverse_1	,ds_Refl_Crack_Transverse_2
,ds_Reflective_Cracking_Long_0	,ds_Reflective_Cracking_Long_1	,ds_Reflective_Cracking_Long_2,ds_Rutting_0	,ds_Rutting_1	,ds_Rutting_2	,ds_Slab_Replacement	,ds_Slab_Replacement_0
,ds_Slab_Replacement_1	,ds_Spalling_Longitudinal_0	,ds_Spalling_Longitudinal_1,ds_Spalling_Longitudinal_2	,ds_Spalling_Transverse_0	,ds_Spalling_Transverse_1
,ds_Spalling_Transverse_2	,ds_Transverse_Cracking_0	,ds_Transverse_Cracking_1,ds_Transverse_Cracking_2	,ds_Slab_Replacement_2'''

            my_dd_keys = '''ID,Name,RoadName,From,To,pvmt_analysis_section_id,dd_Alligator_Cracking_0	,dd_Alligator_Cracking_1	,dd_Alligator_Cracking_2 ,dd_Bleeding_0	,dd_Bleeding_1	,dd_Bleeding_2	,dd_Block_Cracking_0
,dd_Block_Cracking_1	,dd_Block_Cracking_2	,dd_Blowup_0	,dd_Blowup_1,dd_Blowup_2	,dd_Corner_Break_0	,dd_Corner_Break_1	,dd_Corner_Break_2,dd_D_Cracking_0	,dd_D_Cracking_1	,dd_D_Cracking_2	,dd_Edge_Cracking_0
,dd_Edge_Cracking_1	,dd_Edge_Cracking_2	,dd_Faulting_0	,dd_Faulting_1,dd_Faulting_2	,dd_IRI_0	,dd_IRI_1	,dd_IRI_2,dd_Joint_Count_0	,dd_Joint_Count_1	,dd_Joint_Count_2	,dd_Joint_Deterioration_0
,dd_Joint_Deterioration_1	,dd_Joint_Deterioration_2	,dd_Joint_Seal_Deterioration_0,dd_Joint_Seal_Deterioration_1	,dd_Joint_Seal_Deterioration_2	,dd_Lane_Shoulder_Dropoff_0,dd_Lane_Shoulder_Dropoff_1	,dd_Lane_Shoulder_Dropoff_2	,dd_Longitudinal_Cracking_0
,dd_Longitudinal_Cracking_1	,dd_Longitudinal_Cracking_2	,dd_Map_Cracking_0,dd_Map_Cracking_1	,dd_Map_Cracking_2	,dd_Patching_0	,dd_Patching_1	,dd_Patching_2,dd_Potholes_0	,dd_Potholes_1	,dd_Potholes_2	,dd_Pumping_0	,dd_Pumping_1
,dd_Pumping_2	,dd_Punchouts_0	,dd_Punchouts_1	,dd_Punchouts_2	,dd_Punchouts_ph,dd_Raveling_0	,dd_Raveling_1	,dd_Raveling_2	,dd_Refl_Crack_Transverse_0,dd_Refl_Crack_Transverse_1	,dd_Refl_Crack_Transverse_2	,dd_Reflective_Cracking_Long_0
,dd_Reflective_Cracking_Long_1	,dd_Reflective_Cracking_Long_2	,dd_Rutting_0	,dd_Rutting_1,dd_Rutting_2	,dd_Slab_Replacement	,dd_Slab_Replacement_0	,dd_Slab_Replacement_1,dd_Spalling_Longitudinal_0	,dd_Spalling_Longitudinal_1	,dd_Spalling_Longitudinal_2
,dd_Spalling_Transverse_0	,dd_Spalling_Transverse_1	,dd_Spalling_Transverse_2,dd_Transverse_Cracking_0	,dd_Transverse_Cracking_1	,dd_Transverse_Cracking_2,dd_Slab_Replacement_2'''
        
            my_vas_keys2 = []
            for item in my_vas_keys.split(','):
                my_vas_keys2.append(item)

            my_ds_keys2 = []
            for item in my_ds_keys.split(','):
                my_ds_keys2.append(item)

            my_dd_keys2 = []
            for item in my_dd_keys.split(','):
                my_dd_keys2.append(item)

            db = self.my_db_tables.VAnalysis_Sections
            
                    
            stmt = sa.select(db.c.id,db.c.Name,db.c.RoadName,db.c.From,db.c.To,db.c.pvmt_analysis_section_id,db.c.Pavement_A,
db.c.FilterColumn,db.c.maint_dis_nmbr,db.c.FunctionClass,db.c.dd_avg_fault_depth_qty,db.c.dd_avg_iri_qty,
db.c.dd_avg_rut_depth,db.c.dd_distress_rating_nmbr,db.c.dd_faults_qty,db.c.dd_pvmt_condition_rating_nmbr,
db.c.dd_pvmt_section_survey_year,db.c.dd_roughness_rating_nmbr,db.c.data_accum_direction,db.c.dd_data_orientation,
db.c.pvmt_condition_rating_nmbr,db.c.pvmt_type_code,db.c.pvmt_type_desc,db.c.left_shoulder_width_code,
db.c.left_shoulder_width_desc,db.c.right_shoulder_width_code,db.c.right_shoulder_width_desc,
db.c.road_type,db.c.route_id,db.c.pvmt_structure_nmbr,db.c.pvmt_type_code_clustering,db.c.section_lane_cnt,
db.c.section_total_lanes,db.c.survey_avg_lane_width,db.c.total_roadway_width_code,
db.c.total_roadway_width_desc,db.c.county_name,db.c.county_nmbr,db.c.create_date,db.c.create_user,
db.c.update_date,db.c.update_user,db.c.divided_hwy_ind,db.c.Budget_Category_Override,db.c.com_cost,
db.c.com_trt,db.c.com_year,db.c.Comments,db.c.eold,db.c.esal,db.c.RD_Name,db.c.RT_Class,db.c.Reversed,
db.c.sri,db.c.SRI_From,db.c.SRI_To,db.c.Segment,db.c.Segment_Length,db.c.Trt_Family,db.c.Year,db.c.anl_chip_seal,
db.c.anl_rural,db.c.anlss_sctn_annual_flex_esal,db.c.anlss_sctn_annual_rigid_esal,db.c.anlss_sctn_cumul_flex_esal,
db.c.anlss_sctn_cumul_rigid_esal,db.c.begin_english_station_nmbr,db.c.begin_landmark_desc,db.c.begin_lat,db.c.begin_long,
db.c.dFragWithSkip_Cluster,db.c.design_lane_width,db.c.document_id,db.c.end_english_station_nmbr,db.c.end_landmark_desc,
db.c.end_lat,db.c.end_long,db.c.esal_aadt,db.c.esal_flexible_annual,db.c.esal_kip_factor,db.c.esal_pct_trucks,
db.c.esal_rigid_annual,db.c.full_annual_flexible_esal,db.c.full_annual_rigid_esal,db.c.full_cumulative_flexible_esal,
db.c.full_cumulative_rigid_esal,db.c.max_design_hourly_vol,db.c.max_design_hourly_vol_year,
db.c.max_trffc_growth_rate,db.c.max_trffc_section_aadt,db.c.max_trffc_section_aadt_year,
db.c.max_truck_trffc_pct,db.c.measured_section_length,db.c.paved_shoulder_ind,db.c.ph_pvmt_proj_actl_end_date,
db.c.ph_pvmt_rehab_affctd_srfc_pct,db.c.ph_rehab_thickness,db.c.ph_rehab_type_code,db.c.ph_resurfacing_type_code,
db.c.plan_section_length,db.c.pvmt_analysis_section_id_,db.c.pvmt_anlyss_sctn_nhs_ind,db.c.pvmt_mdfd_structure_nmbr,db.c.pvmt_memo,
db.c.pvmt_pre_type_code,db.c.traffic_esal_base_year,db.c.weight
).filter(db.c.RoadName == self.my_sri) 

            if self.FilterColumncheckBox.isChecked() == True:
                stmt = stmt.filter(db.c.FilterColumn == 1)
          
            results1 = self.my_session.execute(stmt)
            
            for item1 in results1:
                my_vas.append(item1)
               



            stmt = sa.select(db.c.id,db.c.Name,db.c.RoadName,db.c.From,db.c.To,db.c.pvmt_analysis_section_id
    ,db.c.ds_Alligator_Cracking_0,db.c.ds_Alligator_Cracking_1,db.c.ds_Alligator_Cracking_2,db.c.ds_Bleeding_0
    ,db.c.ds_Bleeding_1	,db.c.ds_Bleeding_2	,db.c.ds_Block_Cracking_0	,db.c.ds_Block_Cracking_1
    ,db.c.ds_Block_Cracking_2	,db.c.ds_Blowup_0	,db.c.ds_Blowup_1	,db.c.ds_Blowup_2	,db.c.ds_Corner_Break_0
    ,db.c.ds_Corner_Break_1	,db.c.ds_Corner_Break_2	,db.c.ds_D_Cracking_0	,db.c.ds_D_Cracking_1	,db.c.ds_D_Cracking_2
    ,db.c.ds_Edge_Cracking_0	,db.c.ds_Edge_Cracking_1	,db.c.ds_Edge_Cracking_2	,db.c.ds_Faulting_0
    ,db.c.ds_Faulting_1	,db.c.ds_Faulting_2	,db.c.ds_IRI_0	,db.c.ds_IRI_1	,db.c.ds_IRI_2	,db.c.ds_Joint_Count_0
    ,db.c.ds_Joint_Count_1	,db.c.ds_Joint_Count_2	,db.c.ds_Joint_Deterioration_0	,db.c.ds_Joint_Deterioration_1
    ,db.c.ds_Joint_Deterioration_2	,db.c.ds_Joint_Seal_Deterioration_0	,db.c.ds_Joint_Seal_Deterioration_1
    ,db.c.ds_Joint_Seal_Deterioration_2	,db.c.ds_Lane_Shoulder_Dropoff_0	,db.c.ds_Lane_Shoulder_Dropoff_1
    ,db.c.ds_Lane_Shoulder_Dropoff_2	,db.c.ds_Longitudinal_Cracking_0	,db.c.ds_Longitudinal_Cracking_1
    ,db.c.ds_Longitudinal_Cracking_2	,db.c.ds_Map_Cracking_0	,db.c.ds_Map_Cracking_1	,db.c.ds_Map_Cracking_2
    ,db.c.ds_Patching_0	,db.c.ds_Patching_1	,db.c.ds_Patching_2	,db.c.ds_Potholes_0	,db.c.ds_Potholes_1
    ,db.c.ds_Potholes_2	,db.c.ds_Pumping_0	,db.c.ds_Pumping_1	,db.c.ds_Pumping_2	,db.c.ds_Punchouts_0
    ,db.c.ds_Punchouts_1	,db.c.ds_Punchouts_2	,db.c.ds_Raveling_0	,db.c.ds_Raveling_1	,db.c.ds_Raveling_2
    ,db.c.ds_Refl_Crack_Transverse_0	,db.c.ds_Refl_Crack_Transverse_1	,db.c.ds_Refl_Crack_Transverse_2
    ,db.c.ds_Reflective_Cracking_Long_0	,db.c.ds_Reflective_Cracking_Long_1	,db.c.ds_Reflective_Cracking_Long_2
    ,db.c.ds_Rutting_0	,db.c.ds_Rutting_1	,db.c.ds_Rutting_2	,db.c.ds_Slab_Replacement	,db.c.ds_Slab_Replacement_0
    ,db.c.ds_Slab_Replacement_1	,db.c.ds_Spalling_Longitudinal_0	,db.c.ds_Spalling_Longitudinal_1
    ,db.c.ds_Spalling_Longitudinal_2	,db.c.ds_Spalling_Transverse_0	,db.c.ds_Spalling_Transverse_1
    ,db.c.ds_Spalling_Transverse_2	,db.c.ds_Transverse_Cracking_0	,db.c.ds_Transverse_Cracking_1
    ,db.c.ds_Transverse_Cracking_2	,db.c.ds_Slab_Replacement_2).filter(db.c.RoadName == self.my_sri) 

            
            if self.FilterColumncheckBox.isChecked() == True:
                stmt = stmt.filter(db.c.FilterColumn == 1)

            results2 = self.my_session.execute(stmt)
            
            for item2 in results2:
                my_ds.append(item2)
               


            stmt = sa.select(db.c.id,db.c.Name,db.c.RoadName,db.c.From,db.c.To,db.c.pvmt_analysis_section_id
    ,db.c.dd_Alligator_Cracking_0	,db.c.dd_Alligator_Cracking_1	,db.c.dd_Alligator_Cracking_2
    ,db.c.dd_Bleeding_0	,db.c.dd_Bleeding_1	,db.c.dd_Bleeding_2	,db.c.dd_Block_Cracking_0
    ,db.c.dd_Block_Cracking_1	,db.c.dd_Block_Cracking_2	,db.c.dd_Blowup_0	,db.c.dd_Blowup_1
    ,db.c.dd_Blowup_2	,db.c.dd_Corner_Break_0	,db.c.dd_Corner_Break_1	,db.c.dd_Corner_Break_2
    ,db.c.dd_D_Cracking_0	,db.c.dd_D_Cracking_1	,db.c.dd_D_Cracking_2	,db.c.dd_Edge_Cracking_0
    ,db.c.dd_Edge_Cracking_1	,db.c.dd_Edge_Cracking_2	,db.c.dd_Faulting_0	,db.c.dd_Faulting_1
    ,db.c.dd_Faulting_2	,db.c.dd_IRI_0	,db.c.dd_IRI_1	,db.c.dd_IRI_2
    ,db.c.dd_Joint_Count_0	,db.c.dd_Joint_Count_1	,db.c.dd_Joint_Count_2	,db.c.dd_Joint_Deterioration_0
    ,db.c.dd_Joint_Deterioration_1	,db.c.dd_Joint_Deterioration_2	,db.c.dd_Joint_Seal_Deterioration_0
    ,db.c.dd_Joint_Seal_Deterioration_1	,db.c.dd_Joint_Seal_Deterioration_2	,db.c.dd_Lane_Shoulder_Dropoff_0
    ,db.c.dd_Lane_Shoulder_Dropoff_1	,db.c.dd_Lane_Shoulder_Dropoff_2	,db.c.dd_Longitudinal_Cracking_0
    ,db.c.dd_Longitudinal_Cracking_1	,db.c.dd_Longitudinal_Cracking_2	,db.c.dd_Map_Cracking_0
    ,db.c.dd_Map_Cracking_1	,db.c.dd_Map_Cracking_2	,db.c.dd_Patching_0	,db.c.dd_Patching_1	,db.c.dd_Patching_2
    ,db.c.dd_Potholes_0	,db.c.dd_Potholes_1	,db.c.dd_Potholes_2	,db.c.dd_Pumping_0	,db.c.dd_Pumping_1
    ,db.c.dd_Pumping_2	,db.c.dd_Punchouts_0	,db.c.dd_Punchouts_1	,db.c.dd_Punchouts_2	,db.c.dd_Punchouts_ph
    ,db.c.dd_Raveling_0	,db.c.dd_Raveling_1	,db.c.dd_Raveling_2	,db.c.dd_Refl_Crack_Transverse_0
    ,db.c.dd_Refl_Crack_Transverse_1	,db.c.dd_Refl_Crack_Transverse_2	,db.c.dd_Reflective_Cracking_Long_0
    ,db.c.dd_Reflective_Cracking_Long_1	,db.c.dd_Reflective_Cracking_Long_2	,db.c.dd_Rutting_0	,db.c.dd_Rutting_1
    ,db.c.dd_Rutting_2	,db.c.dd_Slab_Replacement	,db.c.dd_Slab_Replacement_0	,db.c.dd_Slab_Replacement_1
    ,db.c.dd_Spalling_Longitudinal_0	,db.c.dd_Spalling_Longitudinal_1	,db.c.dd_Spalling_Longitudinal_2
    ,db.c.dd_Spalling_Transverse_0	,db.c.dd_Spalling_Transverse_1	,db.c.dd_Spalling_Transverse_2
    ,db.c.dd_Transverse_Cracking_0	,db.c.dd_Transverse_Cracking_1	,db.c.dd_Transverse_Cracking_2
    ,db.c.dd_Slab_Replacement_2).filter(db.c.RoadName == self.my_sri).order_by(db.c.RoadName, db.c.From)  
            

            if self.FilterColumncheckBox.isChecked() == True:
                stmt = stmt.filter(db.c.FilterColumn == 1)

            results3 = self.my_session.execute(stmt)

            for item3 in results3:    
                my_dd.append(item3)
                          
         
            self.VAS_tableWidget.clearContents()
            self.VAS_DS_tableWidget.clearContents()
            self.VAS_DD_tableWidget.clearContents()
            
            tableCreate2(self.VAS_tableWidget,my_vas_keys2, my_vas)
            tableCreate2(self.VAS_DS_tableWidget,my_ds_keys2, my_ds)
            tableCreate2(self.VAS_DD_tableWidget,my_dd_keys2, my_dd)
            
            self.VAS_tableWidget.viewport().update()
            self.VAS_DS_tableWidget.viewport().update()
            self.VAS_DD_tableWidget.viewport().update()

            self.tabWidget.setCurrentIndex(0)
            
                     
            
        else:
            pass
        

    def selectRow(self,row,column):
        my_row = row
        my_column = column
        clearColorRow(self.VAS_tableWidget,QtGui.QColor(255,255,255))
        clearColorRow(self.VAS_DS_tableWidget,QtGui.QColor(255,255,255))
        clearColorRow(self.VAS_DD_tableWidget,QtGui.QColor(255,255,255))
        setColorRow(self.VAS_tableWidget,row,QtGui.QColor(211,211,211))
        setColorRow(self.VAS_DS_tableWidget,row,QtGui.QColor(211,211,211))
        setColorRow(self.VAS_DD_tableWidget,row,QtGui.QColor(211,211,211))
        



class VCRH_view(Ui_VCRH_Form):
    def __init__(self, my_self):
        super(VCRH_view, self).__init__()
           
        #self.fileName = 'VCRH'
        self.index = 0
        self.my_login = login_stuff()
        self.my_db_tables = my_self.my_db_tables
        self.my_url = my_self.my_url
        self.database_type = my_self.my_login.database_type
        self.my_session = my_self.my_session
        self.my_login = my_self.my_login

 
        self.my_VAS_Sql = None
        self.my_VAS_DS_Sql = None
        self.my_VAS_DD_Sql = None
        self.my_VAS_Theaders = None
        self.my_VAS_DS_Theaders = None
        self.my_VAS_DD_Theaders = None

        self.my_county = None
        self.my_route = None
        self.my_sri = None
        self.my_from = None
        self.my_to = None

        self.setupUi(self)
        self.setup_county()
       

        self.VCRH_tab.setFocus()

        
        self.comboBoxCounty.currentIndexChanged.connect(self.county_change)
        self.comboBoxRoute.currentIndexChanged.connect(self.route_change)
        self.comboBoxDirection.currentIndexChanged.connect(self.direction_change)
        self.tableWidgetVCRH.cellClicked.connect(self.selectRow)
        self.pushButtonReset.clicked.connect(self.reset_all)
        #self.VCRH_tableView.SelectedClicked.connect(print('Hello'))
    
    def county_change(self):
        if self.comboBoxCounty.currentIndex == 0:
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.setCurrentIndex(0)
        else:
            self.comboBoxRoute.clear()
            self.comboBoxDirection.clear()
            self.setup_route()
            
        pass

    def route_change(self):
        if self.comboBoxRoute.currentIndex == 0:
            
            self.comboBoxDirection.clear()
            pass
        else:
            self.setup_direction()

    def direction_change(self):
        if self.comboBoxDirection.currentIndex == 0  :
            
            pass
        else:
            my_direction = self.comboBoxDirection.currentText()
            if my_direction.strip() == '':
                pass
            else:
                self.my_sri = my_direction[:my_direction.find(' ')]
                self.my_from = my_direction[my_direction.find(': ')+1 : my_direction.find('T') ]
                self.my_from = float(self.my_from.strip())
                self.my_to = my_direction[my_direction.find('To: ')+3:]
                self.my_to = float(self.my_to.strip())
               
                self.fill_tables()
            
                      

        pass
    
    def reset_all(self):
        self.comboBoxCounty.setCurrentIndex(0)
        self.comboBoxRoute.setCurrentIndex(0)
        self.comboBoxDirection.setCurrentIndex(0)
       
       

    def setup_county(self):
        c1 = county_select(self)
        self.comboBoxCounty.addItems(c1.get_county())

    def setup_route(self):
        if self.comboBoxCounty.currentIndex == 0:
            
            self.comboBoxDirection.clear()
            pass
        else:
            rt1 = route_select(self)
            my_temp_list = rt1.get_route()
     
            for item in my_temp_list:
                self.comboBoxRoute.addItem(str(item))     
            self.setup_direction()
            pass       

    def setup_direction(self):
        my_list = []
        if self.comboBoxDirection.currentIndex == 0 :
            
            pass
        else:
            if self.comboBoxRoute.currentIndex != 0:
                db = self.my_db_tables.VBase
                tm_county = self.comboBoxCounty.currentText()
                tm_county = tm_county[tm_county.find('[')+1:tm_county.find(']')]
                tm_route = self.comboBoxRoute.currentText()
                stmt = sa.select(db.c.Name,db.c.From,db.c.To).filter(db.c.County == tm_county).filter(db.c.Route_ID == tm_route).order_by(db.c.Route_ID)
                results = self.my_session.execute(stmt)
            
                my_list.clear()
                my_list.insert(0,'')
                for item in results:
                    if item is None:
                        pass
                    else:
                        my_str = item[0] + ' From: ' + str(item[1]) + ' To: ' + str(item[2])
                        my_list.append(my_str)

            self.comboBoxDirection.clear()        
            self.comboBoxDirection.addItems(my_list) 


    def fill_tables(self):

        if  self.my_VAS_Sql == None:
            self.my_VAS_Sql = None
            self.my_VAS_DS_Sql = None
            self.my_VAS_DD_Sql = None
            self.my_VAS_Theaders = None
            self.my_VAS_DS_Theaders = None
            self.my_VAS_DD_Theaders = None
     
        
            my_CRH_keys = []
            my_CRH_data = []

            db = self.my_db_tables.VConst_Rehab_History
  
            stmt = sa.select(db.c.id,db.c.Name,db.c.RoadName,db.c.From,db.c.To,db.c.pvmt_analysis_section_id,db.c.proj_nmbr,db.c.proj_detail_nmbr
,db.c.pvmt_proj_actl_end_date,db.c.sri,db.c.SRI_From,db.c.SRI_To,db.c.edge_drain_ind,db.c.milling_thickness
,db.c.overlay_data_entered_date,db.c.paving_fabric_ind,db.c.pvmt_analysis_soil_type_code,db.c.pvmt_analysis_soil_type_desc
,db.c.pvmt_rehab_affctd_srfc_pct,db.c.pvmt_structure_removed_ind,db.c.rehab_thickness,db.c.rehab_type_code
,db.c.rehab_type_desc,db.c.resurfacing_type_code,db.c.resurfacing_type_desc,db.c.total_courses_qty
,db.c.total_courses_thickness_qty,db.c.create_date,db.c.create_user,db.c.update_date,db.c.update_user).filter(db.c.RoadName == self.my_sri) 

            results = self.my_session.execute(stmt)

            for item in results.keys():
                my_CRH_keys.append(item)

            for item in results:
                my_CRH_data.append(item)
            
            my_CRLD_keys = []
            my_CRLD_data = []

            db = self.my_db_tables.VConst_Rehab_History
            db2 = self.my_db_tables.VConst_Reh_Lyr_Detail
           
            stmt = sa.select(db2.c.id,db2.c.Name,db2.c.f_szForiegnKey,db2.c.pvmt_analysis_section_id,db2.c.proj_nmbr,db2.c.proj_detail_nmbr
,db2.c.pvmt_course_nmbr,db2.c.pvmt_course_thickness,db2.c.pvmt_layer_material_desc,db2.c.material_type_code
,db2.c.material_type_desc,db2.c.first_material_property,db2.c.first_rehab_material_desc,db2.c.second_material_property
,db2.c.second_rehab_material_desc,db2.c.third_material_property,db2.c.third_rehab_material_desc,db2.c.create_date
,db2.c.create_user,db2.c.update_date,db2.c.update_user).where(db2.c.f_szForiegnKey.in_(sa.select(db.c.Name).filter(db.c.RoadName == self.my_sri)))

            results = self.my_session.execute(stmt)

            for item in results.keys():
                my_CRLD_keys.append(item)    

            for item in results:
                my_CRLD_data.append(item)    
            
            my_proj_keys = []
            my_proj_data = []

            db = self.my_db_tables.VConst_Rehab_History
            db3 = self.my_db_tables.Project

            stmt = sa.select(db3.c.id,db3.c.Name,db3.c.proj_nmbr,db3.c.proj_detail_nmbr,db3.c.pvmt_proj_actl_end_date,db3.c.pvmt_proj_hist_proj_nmbr
,db3.c.pvmt_proj_type,db3.c.create_date,db3.c.create_user,db3.c.update_date,db3.c.update_user,db3.c.pvmt_proj_mix_design_nmbr
,db3.c.skid_test_id, db.c.proj_nmbr,db.c.proj_detail_nmbr).filter(sa.and_(db3.c.proj_nmbr == db.c.proj_nmbr,db3.c.proj_detail_nmbr == db.c.proj_detail_nmbr)).filter(db.c.RoadName == self.my_sri)


            results = self.my_session.execute(stmt)
            for item in results.keys():
                my_proj_keys.append(item)

            results = self.my_session.execute(stmt)
            i=0
            for item in results:
                i=i+1
                my_proj_data.append(item)
               
            
                       
            self.VCRH_tableWidget.clearContents()
            self.VCRLD_tableWidget.clearContents()
            self.Proj_tableWidget.clearContents()
            
            tableCreate2(self.VCRH_tableWidget,my_CRH_keys, my_CRH_data)
            tableCreate2(self.VCRLD_tableWidget,my_CRLD_keys, my_CRLD_data)
            tableCreate2(self.Proj_tableWidget,my_proj_keys, my_proj_data)

            self.VCRH_tableWidget.viewport().update()
            self.VCRLD_tableWidget.viewport().update()
            self.Proj_tableWidget.viewport().update()

            self.tabWidget.setCurrentIndex(0)
                

            
        else:
            pass

    def selectRow(self,row,column):
        my_row = row
        my_column = column
        clearColorRow(self.VCRH_tableWidget,QtGui.QColor(255,255,255))
        clearColorRow(self.VCRLD_tableWidget,QtGui.QColor(255,255,255))
        clearColorRow(self.Proj_tableWidget,QtGui.QColor(255,255,255))

        setColorRow(self.VCRH_tableWidget,row,QtGui.QColor(211,211,211))
        setColorRow(self.VCRLD_tableWidget,row,QtGui.QColor(211,211,211))
        setColorRow(self.Proj_tableWidget,row,QtGui.QColor(211,211,211))    

    def fill_CRLD(self):
        pass

class VCCP_view(Ui_VCRHVCRLDVPROJ_Form):
    def __init__(self, my_self):
        super(VCCP_view, self).__init__()
                
        self.index = 0
        self.my_login = login_stuff()
        self.my_db_tables = my_self.my_db_tables
        self.my_url = my_self.my_url
        self.database_type = my_self.my_login.database_type
        self.my_session = my_self.my_session
        self.my_login = my_self.my_login

 
        self.my_VAS_Sql = None
        self.my_VAS_DS_Sql = None
        self.my_VAS_DD_Sql = None
        self.my_VAS_Theaders = None
        self.my_VAS_DS_Theaders = None
        self.my_VAS_DD_Theaders = None

        self.my_county = None
        self.my_route = None
        self.my_sri = None
        self.my_from = None
        self.my_to = None

        self.setupUi(self)
        self.setup_county()
       
        self.VCRH_tab.setFocus()
        
        self.comboBoxCounty.currentIndexChanged.connect(self.county_change)
        self.comboBoxRoute.currentIndexChanged.connect(self.route_change)
        self.comboBoxDirection.currentIndexChanged.connect(self.direction_change)

        self.VCRH_tableWidget.cellClicked.connect(self.selectRow)
        self.VCRLD_tableWidget.cellClicked.connect(self.selectRow)
        self.Proj_tableWidget.cellClicked.connect(self.selectRow)
        

        self.pushButtonReset.clicked.connect(self.reset_all)
       
    
    def county_change(self):
        if self.comboBoxCounty.currentIndex == 0:
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.setCurrentIndex(0)
        else:
            self.comboBoxRoute.clear()
            self.comboBoxDirection.clear()
            self.setup_route()
            
        pass

    def route_change(self):
        if self.comboBoxRoute.currentIndex == 0:
            
            self.comboBoxDirection.clear()
            pass
        else:
            self.setup_direction()

    def direction_change(self):
        if self.comboBoxDirection.currentIndex == 0  :
            
            pass
        else:
            my_direction = self.comboBoxDirection.currentText()
            if my_direction.strip() == '':
                pass
            else:
                self.my_sri = my_direction[:my_direction.find(' ')]
                self.my_from = my_direction[my_direction.find(': ')+1 : my_direction.find('T') ]
                self.my_from = float(self.my_from.strip())
                self.my_to = my_direction[my_direction.find('To: ')+3:]
                self.my_to = float(self.my_to.strip())
               
                self.fill_tables()
            
                      

        pass
    
    def reset_all(self):
        self.comboBoxCounty.setCurrentIndex(0)
        self.comboBoxRoute.setCurrentIndex(0)
        self.comboBoxDirection.setCurrentIndex(0)
        
       

    def setup_county(self):
        c1 = county_select(self)
        self.comboBoxCounty.addItems(c1.get_county())

    def setup_route(self):
        if self.comboBoxCounty.currentIndex == 0:
            
            self.comboBoxDirection.clear()
            pass
        else:
            rt1 = route_select(self)
            my_temp_list = rt1.get_route()
     
            for item in my_temp_list:
                self.comboBoxRoute.addItem(str(item))     
            self.setup_direction()
            pass       

    def setup_direction(self):
        my_list = []
        if self.comboBoxDirection.currentIndex == 0 :
            
            pass
        else:
            if self.comboBoxRoute.currentIndex != 0:
                db = self.my_db_tables.VBase
                tm_county = self.comboBoxCounty.currentText()
                tm_county = tm_county[tm_county.find('[')+1:tm_county.find(']')]
                tm_route = self.comboBoxRoute.currentText()
                stmt = sa.select(db.c.Name,db.c.From,db.c.To).filter(db.c.County == tm_county).filter(db.c.Route_ID == tm_route).order_by(db.c.Name,db.c.From)
                results = self.my_session.execute(stmt)
            
                my_list.clear()
                my_list.insert(0,'')
                for item in results:
                    if item is None:
                        pass
                    else:
                        my_str = item[0] + ' From: ' + str(item[1]) + ' To: ' + str(item[2])
                        my_list.append(my_str)

            self.comboBoxDirection.clear()        
            self.comboBoxDirection.addItems(my_list) 


    def fill_tables(self):

        if  self.my_VAS_Sql == None:
            self.my_VAS_Sql = None
            self.my_VAS_DS_Sql = None
            self.my_VAS_DD_Sql = None
            self.my_VAS_Theaders = None
            self.my_VAS_DS_Theaders = None
            self.my_VAS_DD_Theaders = None
     
          
            my_CRH_keys = []
      
            my_CRH_data = []

            db = self.my_db_tables.VConst_Rehab_History
  
            stmt = sa.select(db.c.id,db.c.Name,db.c.RoadName,db.c.From,db.c.To,db.c.pvmt_analysis_section_id,db.c.proj_nmbr,db.c.proj_detail_nmbr
,db.c.pvmt_proj_actl_end_date,db.c.edge_drain_ind,db.c.milling_thickness
,db.c.overlay_data_entered_date,db.c.paving_fabric_ind,db.c.pvmt_analysis_soil_type_code,db.c.pvmt_analysis_soil_type_desc
,db.c.pvmt_rehab_affctd_srfc_pct,db.c.pvmt_structure_removed_ind,db.c.rehab_thickness,db.c.rehab_type_code
,db.c.rehab_type_desc,db.c.resurfacing_type_code,db.c.resurfacing_type_desc,db.c.total_courses_qty
,db.c.total_courses_thickness_qty,db.c.create_date,db.c.create_user,db.c.update_date,db.c.update_user).filter(db.c.RoadName == self.my_sri).order_by(db.c.RoadName,db.c.From,db.c.pvmt_proj_actl_end_date.desc()) 

            results = self.my_session.execute(stmt)

            for item in results.keys():
                my_CRH_keys.append(item)

            for item in results:
                my_CRH_data.append(item)

            
            my_CRLD_keys = []
            my_CRLD_data = []

            db = self.my_db_tables.VConst_Rehab_History
            db2 = self.my_db_tables.VConst_Reh_Lyr_Detail
           
            stmt = sa.select(db2.c.id,db.c.RoadName,db.c.From,db.c.To,db.c.pvmt_proj_actl_end_date,db2.c.pvmt_course_nmbr,db2.c.Name,db2.c.pvmt_analysis_section_id,db2.c.proj_nmbr,db2.c.proj_detail_nmbr
,db2.c.pvmt_course_thickness,db2.c.pvmt_layer_material_desc,db2.c.material_type_code,db2.c.material_type_desc,db2.c.first_material_property,db2.c.second_material_property,db2.c.third_material_property
,db2.c.first_rehab_material_desc,db2.c.second_rehab_material_desc,db2.c.third_rehab_material_desc
,db2.c.create_date,db2.c.create_user,db2.c.update_date,db2.c.update_user) \
.where((db2.c.f_szForiegnKey.in_(sa.select(db.c.Name).filter(db.c.RoadName == self.my_sri))),db2.c.f_szForiegnKey == db.c.Name) \
.order_by(db.c.RoadName,db.c.From,db.c.pvmt_proj_actl_end_date.desc(),db2.c.pvmt_course_nmbr.desc()) 

            results = self.my_session.execute(stmt)

            for item in results.keys():
                my_CRLD_keys.append(item)    

            for item in results:
                my_CRLD_data.append(item)    
            
            my_proj_keys = []
            my_proj_data = []

            db = self.my_db_tables.VConst_Rehab_History
            db3 = self.my_db_tables.Project

            stmt = sa.select(db3.c.id, db.c.RoadName,db.c.From,db.c.To,db3.c.Name,db3.c.proj_nmbr,db3.c.proj_detail_nmbr,db3.c.pvmt_proj_actl_end_date,db3.c.pvmt_proj_hist_proj_nmbr
,db3.c.pvmt_proj_type,db3.c.create_date,db3.c.create_user,db3.c.update_date,db3.c.update_user).filter(db.c.RoadName == self.my_sri) \
.where(db.c.proj_nmbr == db3.c.proj_nmbr, db.c.proj_detail_nmbr == db3.c.proj_detail_nmbr) \
.order_by(db.c.RoadName,db.c.From,db3.c.pvmt_proj_actl_end_date.desc())


            results = self.my_session.execute(stmt)
            for item in results.keys():
                my_proj_keys.append(item)

            results = self.my_session.execute(stmt)
            i=0
            for item in results:
                i=i+1
                my_proj_data.append(item)
               
            
                       
            self.VCRH_tableWidget.clearContents()
            self.VCRLD_tableWidget.clearContents()
            self.Proj_tableWidget.clearContents()
            
            tableCreate2(self.VCRH_tableWidget,my_CRH_keys, my_CRH_data)
            tableCreate2(self.VCRLD_tableWidget,my_CRLD_keys, my_CRLD_data)
            tableCreate2(self.Proj_tableWidget,my_proj_keys, my_proj_data)

            self.VCRH_tableWidget.viewport().update()
            self.VCRLD_tableWidget.viewport().update()
            self.Proj_tableWidget.viewport().update()

            self.tabWidget.setCurrentIndex(0)
           
            
        else:
            pass

    def selectRow(self,row,column):
        my_row = row
        my_column = column
        clearColorRow(self.VCRH_tableWidget,QtGui.QColor(255,255,255))
        clearColorRow(self.VCRLD_tableWidget,QtGui.QColor(255,255,255))
        clearColorRow(self.Proj_tableWidget,QtGui.QColor(255,255,255))
        setColorRow(self.VCRH_tableWidget,row,QtGui.QColor(211,211,211))
        setColorRow(self.VCRLD_tableWidget,row,QtGui.QColor(211,211,211))
        setColorRow(self.Proj_tableWidget,row,QtGui.QColor(211,211,211))    
            
    def fill_CRLD(self):
        pass

class VCRH_Edit( Ui_VCRH_Edit_Form):
    def __init__(self,my_self):
        super( VCRH_Edit, self).__init__()
           
 
        self.index = 0
        self.my_login = login_stuff()
        self.my_db_tables = my_self.my_db_tables
        self.my_url = my_self.my_url
        self.database_type = my_self.my_login.database_type
        self.my_session = my_self.my_session
        self.my_login = my_self.my_login
        self.setWindowFlag

        self.my_VAS_Sql = None
        self.my_VAS_DS_Sql = None
        self.my_VAS_DD_Sql = None
        self.my_VAS_Theaders = None
        self.my_VAS_DS_Theaders = None
        self.my_VAS_DD_Theaders = None

        self.my_county = None
        self.my_route = None
        self.my_sri = None
        self.my_from = None
        self.my_to = None

        self.setupUi(self)

        self.setup_county()        

        #self.fgBrush = self.tableWidgetVCRH.item(0,0).forground()
        #self.bgBrush = self.tableWidgetVCRH.item(0,0).background()
       
        self.comboBoxCounty.currentIndexChanged.connect(self.county_change)
        self.comboBoxRoute.currentIndexChanged.connect(self.route_change)
        self.pushButtonReset.clicked.connect(self.reset_all)
        self.comboBoxDirection.currentIndexChanged.connect(self.direction_change)

        self.tableWidgetVCRH.cellClicked.connect(self.selectRow)
               
    def county_change(self):
        if self.comboBoxCounty.currentIndex == 0:
            self.comboBoxRoute.setCurrentIndex(0)
        else:
           
            self.comboBoxRoute.clear()
            self.setup_route()
            
        pass

    def route_change(self):
        if self.comboBoxRoute.currentIndex == 0:
            self.comboBoxDirection.clear()
            self.tableWidgetVCRH.clearContents()
            pass
        else:
           self.setup_route()
        pass

    def direction_change(self):
        if self.comboBoxDirection.currentIndex == 0  :
            
            pass
        else:
            my_direction = self.comboBoxDirection.currentText()
            if my_direction.strip() == '':
                pass
            else:
                self.my_sri = my_direction[:my_direction.find(' ')]
                self.my_from = my_direction[my_direction.find(': ')+1 : my_direction.find('T') ]
                self.my_from = float(self.my_from.strip())
                self.my_to = my_direction[my_direction.find('To: ')+3:]
                self.my_to = float(self.my_to.strip())
               
                self.fill_tables()
                

    def reset_all(self):
        self.comboBoxCounty.setCurrentIndex(0)
        self.comboBoxRoute.setCurrentIndex(0)
        self.comboBoxDirection.clear()
        self.tableWidgetVCRH.clearContents()
   
    def setup_county(self):
        c1 = county_select(self)
        self.comboBoxCounty.addItems(c1.get_county())

    def setup_route(self):
        if self.comboBoxCounty.currentIndex == 0:            
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.clear()
            self.tableWidgetVCRH.clearContents()
            pass
        else:
            rt1 = route_select(self)
            my_temp_list = rt1.get_route()
     
            for item in my_temp_list:
                self.comboBoxRoute.addItem(str(item))     
            self.setup_direction()
            pass       

    def setup_direction(self):
        my_list = []
        if self.comboBoxDirection.currentIndex == 0 :
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.clear()
            self.tableWidgetVCRH.clearContents()
            pass
        else:
            if self.comboBoxRoute.currentIndex != 0:
                db = self.my_db_tables.VBase
                tm_county = self.comboBoxCounty.currentText()
                tm_county = tm_county[tm_county.find('[')+1:tm_county.find(']')]
                tm_route = self.comboBoxRoute.currentText()
                stmt = sa.select(db.c.Name,db.c.From,db.c.To).filter(db.c.County == tm_county).filter(db.c.Route_ID == tm_route).order_by(db.c.Name,db.c.From)
                results = self.my_session.execute(stmt)
            
                my_list.clear()
                my_list.insert(0,'')
                for item in results:
                    if item is None:
                        pass
                    else:
                        my_str = item[0] + ' From: ' + str(item[1]) + ' To: ' + str(item[2])
                        my_list.append(my_str)

            self.comboBoxDirection.clear()        
            self.comboBoxDirection.addItems(my_list) 


    def fill_tables(self):

        if  self.my_VAS_Sql == None:
            self.my_VAS_Sql = None
            self.my_VAS_DS_Sql = None
            self.my_VAS_DD_Sql = None
            self.my_VAS_Theaders = None
            self.my_VAS_DS_Theaders = None
            self.my_VAS_DD_Theaders = None

            my_item = ''  
            my_keys = [] 
            my_data = []
            my_temp = []
            my_vas = []
            my_ds = []
            my_dd = []
            my_hide = []
  
            db = self.my_db_tables.VConst_Rehab_History
            
            stmt = stmt = sa.select(db.c.id,db.c.Name,db.c.RoadName,db.c.From,db.c.To,db.c.pvmt_analysis_section_id,db.c.proj_nmbr,db.c.proj_detail_nmbr
,db.c.pvmt_proj_actl_end_date,db.c.edge_drain_ind,db.c.milling_thickness
,db.c.overlay_data_entered_date,db.c.paving_fabric_ind,db.c.pvmt_analysis_soil_type_code,db.c.pvmt_analysis_soil_type_desc
,db.c.pvmt_rehab_affctd_srfc_pct,db.c.pvmt_structure_removed_ind,db.c.rehab_thickness,db.c.rehab_type_code
,db.c.rehab_type_desc,db.c.resurfacing_type_code,db.c.resurfacing_type_desc,db.c.total_courses_qty
,db.c.total_courses_thickness_qty,db.c.create_date,db.c.create_user,db.c.update_date,db.c.update_user).filter(db.c.RoadName == self.my_sri).order_by(db.c.RoadName,db.c.From,db.c.pvmt_proj_actl_end_date.desc()) 
          
            results = self.my_session.execute(stmt)

            for item in results.keys():
                my_keys.append(item)
                

                        
            for item in results:
                my_data.append(item)
                    
               
            self.tableWidgetVCRH.clearContents()
               
            tableCreate2(self.tableWidgetVCRH,my_keys, my_data)
                   
               
            self.tableWidgetVCRH.viewport().update()
     
            
        else:
            pass

    def selectRow(self,row,column):
        my_row = row
        my_column = column
        clearColorRow(self.tableWidgetVCRH,QtGui.QColor(255,255,255))
        setColorRow(self.tableWidgetVCRH,row,QtGui.QColor(211,211,211))
        self.transToEdit(row)

    def transToEdit(self,row):
        for j in range(self.tableWidgetVCRH.columnCount()):
            my_item = self.tableWidgetVCRH.horizontalHeaderItem(j).text()
            if my_item == 'id':
                self.textEditid.setPlainText(  self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'Name':
                self.textEditName.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'From':
                self.textEditFrom.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'To':
                self.textEditTo.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'To':
                self.textEditTo.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'pvmt_analysis_section_id':
                self.textEditpasid.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'proj_nmbr':
                self.textEditproj_nmbr.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'proj_detail_nmbr':
                self.textEditproj_detail_nmbr.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'pvmt_analysis_soil_type_code':
                self.textEditsoil_type_code.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'pvmt_analysis_soil_type_desc':
                self.textEditsoil_type_desc.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'pvmt_rehab_affctd_srfc_pct':
                self.textEditrehab_affctd_srfc_pct.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'rehab_thickness':
                self.textEditrehab_thickness.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'rehab_type_code':
                self.textEditrehab_type_code.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'rehab_type_desc':
                self.textEditrehab_type_desc.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'resurfacing_type_code':
                self.textEditresurfacing_type_code.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'resurfacing_type_desc':
                self.textEditresurfacing_type_desc.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'milling_thickness':
                self.textEditmilling_thickness.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'total_courses_qty':
                self.textEdittotal_courses_qty.setPlainText(self.tableWidgetVCRH.item(row,j).text())
            elif my_item == 'total_courses_thickness_qty':
                self.textEdittotal_courses_thickness_qty.setPlainText(self.tableWidgetVCRH.item(row,j).text())


            else:
                pass


class VProj_Edit(Ui_VProj_Edit_Form):
    def __init__(self,my_self):
        super( VProj_Edit, self).__init__()
           
 
        self.index = 0
        self.my_login = login_stuff()
        self.my_db_tables = my_self.my_db_tables
        self.my_url = my_self.my_url
        self.database_type = my_self.my_login.database_type
        self.my_session = my_self.my_session
        self.my_login = my_self.my_login
        self.setWindowFlag

        self.my_VAS_Sql = None
        self.my_VAS_DS_Sql = None
        self.my_VAS_DD_Sql = None
        self.my_VAS_Theaders = None
        self.my_VAS_DS_Theaders = None
        self.my_VAS_DD_Theaders = None

        self.my_county = None
        self.my_route = None
        self.my_sri = None
        self.my_from = None
        self.my_to = None

        self.setupUi(self)

        self.setup_county()        
       
        self.comboBoxCounty.currentIndexChanged.connect(self.county_change)
        self.comboBoxRoute.currentIndexChanged.connect(self.route_change)
        self.pushButtonReset.clicked.connect(self.reset_all)
        self.comboBoxDirection.currentIndexChanged.connect(self.direction_change)
        self.tableWidget.cellClicked.connect(self.selectRow)
               
    def county_change(self):
        if self.comboBoxCounty.currentIndex == 0:
            self.comboBoxRoute.setCurrentIndex(0)
        else:
           
            self.comboBoxRoute.clear()
            self.setup_route()
            
        pass

    def route_change(self):
        if self.comboBoxRoute.currentIndex == 0:
            self.comboBoxDirection.clear()
            self.tableWidgetVCRH.clearContents()
            pass
        else:
           self.setup_route()
        pass

    def direction_change(self):
        if self.comboBoxDirection.currentIndex == 0  :
            
            pass
        else:
            my_direction = self.comboBoxDirection.currentText()
            if my_direction.strip() == '':
                pass
            else:
                self.my_sri = my_direction[:my_direction.find(' ')]
                self.my_from = my_direction[my_direction.find(': ')+1 : my_direction.find('T') ]
                self.my_from = float(self.my_from.strip())
                self.my_to = my_direction[my_direction.find('To: ')+3:]
                self.my_to = float(self.my_to.strip())
               
                self.fill_tables()
                

    def reset_all(self):
        self.comboBoxCounty.setCurrentIndex(0)
        self.comboBoxRoute.setCurrentIndex(0)
        self.comboBoxDirection.clear()
        self.tableWidget.clearContents()
   
    def setup_county(self):
        c1 = county_select(self)
        self.comboBoxCounty.addItems(c1.get_county())

    def setup_route(self):
        if self.comboBoxCounty.currentIndex == 0:            
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.clear()
            self.tableWidgetVCRH.clearContents()
            pass
        else:
            rt1 = route_select(self)
            my_temp_list = rt1.get_route()
     
            for item in my_temp_list:
                self.comboBoxRoute.addItem(str(item))     
            self.setup_direction()
            pass       

    def setup_direction(self):
        my_list = []
        if self.comboBoxDirection.currentIndex == 0 :
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.clear()
            self.tableWidgetVCRH.clearContents()
            pass
        else:
            if self.comboBoxRoute.currentIndex != 0:
                db = self.my_db_tables.VBase
                tm_county = self.comboBoxCounty.currentText()
                tm_county = tm_county[tm_county.find('[')+1:tm_county.find(']')]
                tm_route = self.comboBoxRoute.currentText()
                stmt = sa.select(db.c.Name,db.c.From,db.c.To).filter(db.c.County == tm_county).filter(db.c.Route_ID == tm_route).order_by(db.c.Name,db.c.From)
                results = self.my_session.execute(stmt)
            
                my_list.clear()
                my_list.insert(0,'')
                for item in results:
                    if item is None:
                        pass
                    else:
                        my_str = item[0] + ' From: ' + str(item[1]) + ' To: ' + str(item[2])
                        my_list.append(my_str)

            self.comboBoxDirection.clear()        
            self.comboBoxDirection.addItems(my_list) 


    def fill_tables(self):

        if  self.my_VAS_Sql == None:
            self.my_VAS_Sql = None
            self.my_VAS_DS_Sql = None
            self.my_VAS_DD_Sql = None
            self.my_VAS_Theaders = None
            self.my_VAS_DS_Theaders = None
            self.my_VAS_DD_Theaders = None

            my_item = ''  
            my_keys = [] 
            my_data = []
            my_temp = []
            my_vas = []
            my_ds = []
            my_dd = []
            my_hide = []
  
            db = self.my_db_tables.VProject
             
            my_keys = []
            my_data = []

            db = self.my_db_tables.VConst_Rehab_History
            db3 = self.my_db_tables.Project

            stmt = sa.select(db3.c.id,db3.c.Name,db3.c.proj_nmbr,db3.c.proj_detail_nmbr,db3.c.pvmt_proj_actl_end_date,db3.c.pvmt_proj_hist_proj_nmbr
,db3.c.pvmt_proj_type,db3.c.create_date,db3.c.create_user,db3.c.update_date,db3.c.update_user,db3.c.pvmt_proj_mix_design_nmbr
,db3.c.skid_test_id, db.c.proj_nmbr,db.c.proj_detail_nmbr).filter(sa.and_(db3.c.proj_nmbr == db.c.proj_nmbr,db3.c.proj_detail_nmbr == db.c.proj_detail_nmbr)).filter(db.c.RoadName == self.my_sri)

 
            results = self.my_session.execute(stmt)

            for item in results.keys():
                my_keys.append(item)
                
                        
            for item in results:
                my_data.append(item)
                    
               
            self.tableWidget.clearContents()
            tableCreate2(self.tableWidget,my_keys, my_data)   
                
            self.tableWidget.viewport().update()
     
            
        else:
            pass

    def selectRow(self,row,column):
        my_row = row
        my_column = column
        clearColorRow(self.tableWidget,QtGui.QColor(255,255,255))
        setColorRow(self.tableWidget,row,QtGui.QColor(211,211,211))

class VCRLD_Edit(Ui_VCRLD_Edit_Form):
    def __init__(self,my_self):
        super(VCRLD_Edit, self).__init__()
           
 
        self.index = 0
        self.my_login = login_stuff()
        self.my_db_tables = my_self.my_db_tables
        self.my_url = my_self.my_url
        self.database_type = my_self.my_login.database_type
        self.my_session = my_self.my_session
        self.my_login = my_self.my_login
        self.setWindowFlag

        self.my_VAS_Sql = None
        self.my_VAS_DS_Sql = None
        self.my_VAS_DD_Sql = None
        self.my_VAS_Theaders = None
        self.my_VAS_DS_Theaders = None
        self.my_VAS_DD_Theaders = None

        self.my_county = None
        self.my_route = None
        self.my_sri = None
        self.my_from = None
        self.my_to = None

        self.setupUi(self)

        self.setup_county()        
       
        self.comboBoxCounty.currentIndexChanged.connect(self.county_change)
        self.comboBoxRoute.currentIndexChanged.connect(self.route_change)
        self.pushButtonReset.clicked.connect(self.reset_all)
        self.comboBoxDirection.currentIndexChanged.connect(self.direction_change)
        self.tableWidget.cellClicked.connect(self.selectRow)
               
    def county_change(self):
        if self.comboBoxCounty.currentIndex == 0:
            self.comboBoxRoute.setCurrentIndex(0)
        else:
           
            self.comboBoxRoute.clear()
            self.setup_route()
            
        pass

    def route_change(self):
        if self.comboBoxRoute.currentIndex == 0:
            self.comboBoxDirection.clear()
            self.tableWidgetVCRH.clearContents()
            pass
        else:
           self.setup_route()
        pass

    def direction_change(self):
        if self.comboBoxDirection.currentIndex == 0  :
            
            pass
        else:
            my_direction = self.comboBoxDirection.currentText()
            if my_direction.strip() == '':
                pass
            else:
                self.my_sri = my_direction[:my_direction.find(' ')]
                self.my_from = my_direction[my_direction.find(': ')+1 : my_direction.find('T') ]
                self.my_from = float(self.my_from.strip())
                self.my_to = my_direction[my_direction.find('To: ')+3:]
                self.my_to = float(self.my_to.strip())
               
                self.fill_tables()
                

    def reset_all(self):
        self.comboBoxCounty.setCurrentIndex(0)
        self.comboBoxRoute.setCurrentIndex(0)
        self.comboBoxDirection.clear()
        self.tableWidget.clearContents()
   
    def setup_county(self):
        c1 = county_select(self)
        self.comboBoxCounty.addItems(c1.get_county())

    def setup_route(self):
        if self.comboBoxCounty.currentIndex == 0:            
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.clear()
            self.tableWidget.clearContents()
            pass
        else:
            rt1 = route_select(self)
            my_temp_list = rt1.get_route()
     
            for item in my_temp_list:
                self.comboBoxRoute.addItem(str(item))     
            self.setup_direction()
            pass       

    def setup_direction(self):
        my_list = []
        if self.comboBoxDirection.currentIndex == 0 :
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.clear()
            self.tableWidget.clearContents()
            pass
        else:
            if self.comboBoxRoute.currentIndex != 0:
                db = self.my_db_tables.VBase
                tm_county = self.comboBoxCounty.currentText()
                tm_county = tm_county[tm_county.find('[')+1:tm_county.find(']')]
                tm_route = self.comboBoxRoute.currentText()
                stmt = sa.select(db.c.Name,db.c.From,db.c.To).filter(db.c.County == tm_county).filter(db.c.Route_ID == tm_route).order_by(db.c.Name,db.c.From)
                results = self.my_session.execute(stmt)
            
                my_list.clear()
                my_list.insert(0,'')
                for item in results:
                    if item is None:
                        pass
                    else:
                        my_str = item[0] + ' From: ' + str(item[1]) + ' To: ' + str(item[2])
                        my_list.append(my_str)

            self.comboBoxDirection.clear()        
            self.comboBoxDirection.addItems(my_list) 


    def fill_tables(self):

        if  self.my_VAS_Sql == None:
            self.my_VAS_Sql = None
            self.my_VAS_DS_Sql = None
            self.my_VAS_DD_Sql = None
            self.my_VAS_Theaders = None
            self.my_VAS_DS_Theaders = None
            self.my_VAS_DD_Theaders = None

                           
            my_keys = []
            my_data = []

            db = self.my_db_tables.VConst_Rehab_History
            db2 = self.my_db_tables.VConst_Reh_Lyr_Detail
           
            stmt = sa.select(db2.c.id,db.c.RoadName,db.c.From,db.c.To,db.c.pvmt_proj_actl_end_date,db2.c.pvmt_course_nmbr,db2.c.Name,db2.c.pvmt_analysis_section_id,db2.c.proj_nmbr,db2.c.proj_detail_nmbr
,db2.c.pvmt_course_thickness,db2.c.pvmt_layer_material_desc,db2.c.material_type_code,db2.c.material_type_desc,db2.c.first_material_property,db2.c.second_material_property,db2.c.third_material_property
,db2.c.first_rehab_material_desc,db2.c.second_rehab_material_desc,db2.c.third_rehab_material_desc
,db2.c.create_date,db2.c.create_user,db2.c.update_date,db2.c.update_user) \
.where((db2.c.f_szForiegnKey.in_(sa.select(db.c.Name).filter(db.c.RoadName == self.my_sri))),db2.c.f_szForiegnKey == db.c.Name) \
.order_by(db.c.RoadName,db.c.From,db.c.pvmt_proj_actl_end_date.desc(),db2.c.pvmt_course_nmbr.desc()) 

            results = self.my_session.execute(stmt)

            for item in results.keys():
                my_keys.append(item)
                
                        
            for item in results:
                my_data.append(item)
                    
               
            self.tableWidget.clearContents()
            tableCreate2(self.tableWidget,my_keys, my_data)   
            self.tableWidget.viewport().update()
     
            
        else:
            pass

    def selectRow(self,row,column):
        my_row = row
        my_column = column
        clearColorRow(self.tableWidget,QtGui.QColor(255,255,255))
        setColorRow(self.tableWidget,row,QtGui.QColor(211,211,211))
      
class RPE_Edit(Ui_rtProjEntryForm):
    def __init__(self,my_self):
        super(Ui_rtProjEntryForm, self).__init__()
           
 
        self.index = 0
        self.my_login = login_stuff()
        self.my_db_tables = my_self.my_db_tables
        self.my_url = my_self.my_url
        self.database_type = my_self.my_login.database_type
        self.my_session = my_self.my_session
        self.my_login = my_self.my_login
        self.setWindowFlag

        self.my_VAS_Sql = None
        self.my_VAS_DS_Sql = None
        self.my_VAS_DD_Sql = None
        self.my_VAS_Theaders = None
        self.my_VAS_DS_Theaders = None
        self.my_VAS_DD_Theaders = None

        self.my_county = None
        self.my_route = None
        self.my_sri = None
        self.my_from = None
        self.my_to = None

        self.setupUi(self)

        self.setup_county()        
       
        self.comboBoxCounty.currentIndexChanged.connect(self.county_change)
        self.comboBoxRoute.currentIndexChanged.connect(self.route_change)
        self.pushButtonReset.clicked.connect(self.reset_all)
        self.comboBoxDirection.currentIndexChanged.connect(self.direction_change)
        self.tableWidget.cellClicked.connect(self.selectRow)
               
    def county_change(self):
        if self.comboBoxCounty.currentIndex == 0:
            self.comboBoxRoute.setCurrentIndex(0)
        else:
           
            self.comboBoxRoute.clear()
            self.setup_route()
            
        pass

    def route_change(self):
        if self.comboBoxRoute.currentIndex == 0:
            self.comboBoxDirection.clear()
            self.tableWidgetVCRH.clearContents()
            pass
        else:
           self.setup_route()
        pass

    def direction_change(self):
        if self.comboBoxDirection.currentIndex == 0  :
            
            pass
        else:
            my_direction = self.comboBoxDirection.currentText()
            if my_direction.strip() == '':
                pass
            else:
                self.my_sri = my_direction[:my_direction.find(' ')]
                self.my_from = my_direction[my_direction.find(': ')+1 : my_direction.find('T') ]
                self.my_from = float(self.my_from.strip())
                self.my_to = my_direction[my_direction.find('To: ')+3:]
                self.my_to = float(self.my_to.strip())
               
                self.fill_tables()
                

    def reset_all(self):
        self.comboBoxCounty.setCurrentIndex(0)
        self.comboBoxRoute.setCurrentIndex(0)
        self.comboBoxDirection.clear()
        self.tableWidget.clearContents()
   
    def setup_county(self):
        c1 = county_select(self)
        self.comboBoxCounty.addItems(c1.get_county())

    def setup_route(self):
        if self.comboBoxCounty.currentIndex == 0:            
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.clear()
            self.tableWidget.clearContents()
            pass
        else:
            rt1 = route_select(self)
            my_temp_list = rt1.get_route()
     
            for item in my_temp_list:
                self.comboBoxRoute.addItem(str(item))     
            self.setup_direction()
            pass       

    def setup_direction(self):
        my_list = []
        if self.comboBoxDirection.currentIndex == 0 :
            self.comboBoxRoute.setCurrentIndex(0)
            self.comboBoxDirection.clear()
            self.tableWidget.clearContents()
            pass
        else:
            if self.comboBoxRoute.currentIndex != 0:
                db = self.my_db_tables.VBase
                tm_county = self.comboBoxCounty.currentText()
                tm_county = tm_county[tm_county.find('[')+1:tm_county.find(']')]
                tm_route = self.comboBoxRoute.currentText()
                stmt = sa.select(db.c.Name,db.c.From,db.c.To).filter(db.c.County == tm_county).filter(db.c.Route_ID == tm_route).order_by(db.c.Name,db.c.From)
                results = self.my_session.execute(stmt)
            
                my_list.clear()
                my_list.insert(0,'')
                for item in results:
                    if item is None:
                        pass
                    else:
                        my_str = item[0] + ' From: ' + str(item[1]) + ' To: ' + str(item[2])
                        my_list.append(my_str)

            self.comboBoxDirection.clear()        
            self.comboBoxDirection.addItems(my_list) 


    def fill_tables(self):

        if  self.my_VAS_Sql == None:
            self.my_VAS_Sql = None
            self.my_VAS_DS_Sql = None
            self.my_VAS_DD_Sql = None
            self.my_VAS_Theaders = None
            self.my_VAS_DS_Theaders = None
            self.my_VAS_DD_Theaders = None

            my_item = ''  
            my_keys = [] 
            my_data = []
            my_temp = []
            my_vas = []
            my_ds = []
            my_dd = []
            my_hide = []
  
            db = self.my_db_tables.VProject
             
            my_keys = []
            my_data = []

            db = self.my_db_tables.VConst_Rehab_History
            db3 = self.my_db_tables.Project

            stmt = sa.select(db3.c.id,db3.c.Name,db3.c.proj_nmbr,db3.c.proj_detail_nmbr,db3.c.pvmt_proj_actl_end_date,db3.c.pvmt_proj_hist_proj_nmbr
,db3.c.pvmt_proj_type,db3.c.create_date,db3.c.create_user,db3.c.update_date,db3.c.update_user,db3.c.pvmt_proj_mix_design_nmbr
,db3.c.skid_test_id, db.c.proj_nmbr,db.c.proj_detail_nmbr).filter(sa.and_(db3.c.proj_nmbr == db.c.proj_nmbr,db3.c.proj_detail_nmbr == db.c.proj_detail_nmbr)).filter(db.c.RoadName == self.my_sri)

 
            results = self.my_session.execute(stmt)

            for item in results.keys():
                my_keys.append(item)
                
                        
            for item in results:
                my_data.append(item)
                    
               
            self.tableWidget.clearContents()
            tableCreate2(self.tableWidget,my_keys, my_data)   
                
            self.tableWidget.viewport().update()
     
            
        else:
            pass

    def selectRow(self,row,column):
        my_row = row
        my_column = column
        clearColorRow(self.tableWidget,QtGui.QColor(255,255,255))
        setColorRow(self.tableWidget,row,QtGui.QColor(211,211,211))
    
             
 
if __name__ == '__main__':
    app = QApplication(sys.argv)

    form =   VAS_Edit()
    form.show()

    sys.exit(app.exec())
