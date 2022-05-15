import os
import sys
import glob
import argparse
import configparser
import shutil


class DtccValidation():

    def __init__(self):
        '''
        Validates DTCC POV ,FAR and COM
        .'''
        
        self.file_type = None
        self.folder_path_already_sent_file = None
        self.folder_path_current_file = None
        self.file_path = None
        self.participant_number_check = True
        self.ips_business_code_check = True
        self.transmission_id_check = True
        self.ips_ind_check = True
        self.submitting_header_count_check = True
        self.subumitted_contract_count_check = True
        self.delivered_contract_count_check = True
        self.datatrak_count_check = True
        self.nscc_control_number_check =True
        self.transmission_id_list = []
        self.nscc_control_number_list = []
        self.submitting_headers_result = {}
        self.data_trak_header_result = {}
        self.conta_headers_result = {}
        self.transmission_id_results = {}
        self.nscc_control_number_results = {}
        self.read_arguemnts()
    
    def read_arguemnts(self):
        
        print("read_arguemnts() Execution Started")
        
        parser = argparse.ArgumentParser()
        parser.add_argument("--file_type", required = True, choices = ['FAR', 'COM', 'POV'],
                             help = "File type like POV , FAR or COM upper case")
        parser.add_argument("--folder_path_already_sent_file", required = True,
                             help = "Absolute path of the folder which contains already sent file details \
                             Windows eg: C:\\Users\Deepak\Downloads\DTCC Linux eg: /usr/bin/Deepak/DTCC ")
        parser.add_argument("--folder_path_current_file", required = True,
                             help = "Absolute path of the folder which contains current file which needs to be validated \
                             Windows eg: C:\\Users\Deepak\Downloads\DTCC Linux eg: /usr/bin/Deepak/DTCC ")
        argument = parser.parse_args()
        self.file_type = argument.file_type
        self.folder_path_already_sent_file = argument.folder_path_already_sent_file
        self.folder_path_current_file = argument.folder_path_current_file
        
        for folder_path in [self.folder_path_already_sent_file, self.folder_path_current_file]:
            if not os.path.isdir(folder_path):
                print(f' Invalid folder path or Folder path is not present  {folder_path} hence terminating')
                exit(0)
        
        print(f' File type  {self.file_type}')
        print(f' Folder path folder_path_already_sent_file {self.folder_path_already_sent_file}')
        print(f' Folder path folder_path_current_file {self.folder_path_current_file}')
        
        print("read_arguemnts() Execution Completed")
        self.process_starts()
        
            
    def process_starts(self):
        
        
        print("process_starts() Execution Started")
        print(f' Validation Started for the File type  {self.file_type}')
        print(f"process_starts() Current input file validation which is present at the location {self.folder_path_current_file}")

        for file in glob.glob(os.path.join(self.folder_path_current_file,"*.txt")):
            self.file_path = file

        if self.file_path is None:
            print(f' No input file which is having *.txt at the end is not present at the location {self.folder_path_current_file} hence terminating ')
            exit(0)

        print(f' Validation of the file  {self.file_type} has started')

        self.submitting_header_validation(self.file_path)
        self.contra_header_validaton(self.file_path)
        print(self.submitting_headers_result.values())
        print(self.data_trak_header_result.values())
        print(self.conta_headers_result.values())
        print(self.nscc_control_number_list)
        print(self.transmission_id_list)
        self.previous_file_records_check()
        print(self.transmission_id_results)
        print(self.nscc_control_number_results)
        print(os.getcwd())
        
        folder_path = os.getcwd()
        final_folder_path = os.path.join(folder_path, "Output")
        
        if os.path.isdir(final_folder_path):
            shutil.rmtree(final_folder_path)
            os.mkdir(final_folder_path)
        else:
            os.mkdir(final_folder_path)
    

        fp = open(os.path.join(final_folder_path, "ValidationResult.txt"), 'w')

        fp.write("\n\n")
        fp.write("----------------------------------------------------------------------------------------------------------------------------- \n")
        fp.write(f'\t\t\t\t\t\t\t\t\t\t\t DTCC Validation Result for {self.file_type}\n')
        fp.write("----------------------------------------------------------------------------------------------------------------------------- \n\n\n\n")
        fp.write("----------------------------------------------\n")
        fp.write("Datatrak Header Validation Result\n")
        fp.write("----------------------------------------------\n\n")
        
        for outside_key, values in self.data_trak_header_result.items():
            for inside_key, value in values.items():
                fp.write(str(inside_key)+"\t=\t"+str(value)+"\n")
        
        fp.write("\n\n")
        fp.write("----------------------------------------------\n")
        fp.write("Submitting Header Validation Result\n")
        fp.write("----------------------------------------------\n\n")
        fp.write(f'Total number of Submitting Headers in the file {len(self.submitting_headers_result)} \n\n\n')
        
        index = 1
        for outside_key, values in self.submitting_headers_result.items():
            fp.write(f'Submitting Header {index} Result\n\n')
            fp.write(outside_key+"\n")
            for inside_key, value in values.items():
                fp.write(str(inside_key)+"\t=\t"+str(value)+"\n")
            fp.write("\n\n")
            index += 1
        
        fp.write("----------------------------------------------\n")
        fp.write("Contra Header Validation Result\n")
        fp.write("----------------------------------------------\n\n")
        
        index = 1
        for outside_key, values in self.conta_headers_result.items():
            fp.write(f'Contra Header {index} Result\n\n')
            fp.write(outside_key+"\n")
            for inside_key, value in values.items():
                fp.write(str(inside_key)+"\t=\t"+str(value)+"\n")
            fp.write("\n\n")
            index += 1
            
        
        fp.write("----------------------------------------------\n")
        fp.write("Transmission ID Previous File Validation Result\n")
        fp.write("----------------------------------------------\n\n")
        
        index = 1
        for outside_key, values in self.transmission_id_results.items():
            fp.write(f'Transmission ID {index} Result\n\n')
            fp.write(outside_key+"\n\n")
            for inside_key, value in values.items():
                fp.write(str(inside_key)+"\t=\t"+str(value)+"\n")
            fp.write("\n\n")
            index += 1
        
        self.transmission_id_list = list(set(self.transmission_id_list))
        
        for transmission_id in self.transmission_id_list:
            if transmission_id not in self.transmission_id_results:
                fp.write(f'Transmission ID {index} Result\n\n')
                fp.write(transmission_id+"\n\n")
                index += 1
                final_dict =  {"transmission_id" : transmission_id, "transmission_id_compare_result": "Not Used in Previous file"}
                for inside_key, value in final_dict.items():
                    fp.write(str(inside_key)+"\t=\t"+str(value)+"\n")
                fp.write("\n\n")
        
        fp.write("----------------------------------------------\n")
        fp.write("NSCC Control Number Previous File Validation Result\n")
        fp.write("----------------------------------------------\n\n")
        
        index = 1
        for outside_key, values in self.nscc_control_number_results.items():
            fp.write(f'NSCC Number {index} Result\n\n')
            fp.write(outside_key+"\n\n")
            for inside_key, value in values.items():
                fp.write(str(inside_key)+"\t=\t"+str(value)+"\n")
            fp.write("\n\n")
            index += 1
        
        self.nscc_control_number_list = list(set(self.nscc_control_number_list))

        for nscc_control_number in self.nscc_control_number_list:
            if nscc_control_number not in self.nscc_control_number_results:
                fp.write(f'NSCC Number {index} Result\n\n')
                fp.write(nscc_control_number+"\n\n")
                index += 1
                final_dict =   {"nscc_control_number" : nscc_control_number, "line_nscc_control_number_result": "Not Used in Previous file"}
                for inside_key, value in final_dict.items():
                    fp.write(str(inside_key)+"\t=\t"+str(value)+"\n")
                fp.write("\n\n")
        
        fp.close()
        
        
        print("process_starts() Execution Completed")
        
    
    def previous_file_records_check(self):
        
        print("previous_file_records_check() Execution Started")
        
        nscc_control_rec_dtls =  {'COM' : {'start': 6, 'end': 25, 'length' : 20, 'contract': 'C2201'},
                                   'FAR' : {'start': 36, 'end': 55, 'length' : 20, 'contract': 'C4305'}
                                   }
        
        transmission_id_rec_dtls =  {'COM' : {'start': 11, 'end': 40, 'length' : 30, 'record': 'C20'},
                                     'POV' : {'start': 11, 'end': 40, 'length' : 30, 'record': 'C10',
                                     'FAR' : {'start': 4, 'end': 33, 'length' : 30, 'record': 'C40'}
                                     }}
        
        
        for file in glob.glob(os.path.join(self.folder_path_already_sent_file,"*.txt")):

            fp = open(file)

            for line in fp:
                
                line_record = line[0:3]
                submitting_record = transmission_id_rec_dtls[self.file_type]['record']
                line_record_contract = line[0:5]

                if line_record == submitting_record:
                    
                    start = transmission_id_rec_dtls[self.file_type]['start']
                    end =  transmission_id_rec_dtls[self.file_type]['end']
                    
                    line_transmission_id = line[start-1:end]
                    line_transmission_id = line_transmission_id.strip()
                    
                    if line_transmission_id in self.transmission_id_list:
                        self.transmission_id_results[line_transmission_id] = {"transmission_id" : line_transmission_id, "transmission_id_compare_result": "Already Used in Previous file", "file_location": file}

                elif self.file_type in ["COM", "FAR"] and line_record_contract == nscc_control_rec_dtls[self.file_type]["contract"]:
                
                    start = nscc_control_rec_dtls[self.file_type]['start']
                    end =  nscc_control_rec_dtls[self.file_type]['end']
                    
                    line_nscc_control_number = line[start-1:end]
                    line_nscc_control_number = line_nscc_control_number.strip()

                    if line_nscc_control_number in self.nscc_control_number_list:
                        self.nscc_control_number_results[line_nscc_control_number] = {"nscc_control_number" : line_nscc_control_number, "line_nscc_control_number_result": "Already Used in Previous file", "file_location": file}

                    
            fp.close()
                
        
        print("previous_file_records_check() Execution Completed")
        
        
    def contra_header_validaton(self, file_path):
        
        print("contra_header_validaton() Execution Started")

        submitted_crt_cnt_dtls =  {'COM' : {'start': 12, 'end': 21, 'length' : 10, 'record': 'C21', 'contract': 'C2201', 'submitting_header': 'C20'},
                                   'POV' : {'start': 12, 'end': 21, 'length' : 10, 'record': 'C12', 'contract': 'C1301', 'submitting_header': 'C10'},
                                   'FAR' : {'start': 12, 'end': 21, 'length' : 10, 'record': 'C42', 'contract': 'C4301', 'submitting_header': 'C40'}
                                   }
        
        delivered_crt_cnt_dtls =  {'COM' : {'start': 22, 'end': 31, 'length' : 10, 'record': 'C21','contract': 'C2201', 'submitting_header': 'C20'},
                                   'POV' : {'start': 22, 'end': 31, 'length' : 10, 'record': 'C12', 'contract': 'C1301', 'submitting_header': 'C10'},
                                   'FAR' : {'start': 22, 'end': 31, 'length' : 10, 'record': 'C42', 'contract': 'C4301', 'submitting_header': 'C40'}
                                   }
        
        nscc_control_rec_dtls =  {'COM' : {'start': 6, 'end': 25, 'length' : 20, 'contract': 'C2201'},
                                   'FAR' : {'start': 36, 'end': 55, 'length' : 20, 'contract': 'C4305'}
                                   }
        
        fp = open(file_path)
        
        contra_header_cnt = 0
        previous_contra_header = None
            
        for line in fp:
            
            self.nscc_control_number_check = True
            self.subumitted_contract_count_check = True
            self.delivered_contract_count_check = True
            self.datatrak_count_check = True
            
            if line[0:3] == "HDR":
                continue
            
            contra_header_record = submitted_crt_cnt_dtls[self.file_type]['record']
            contract_header = submitted_crt_cnt_dtls[self.file_type]['contract']
            submitting_header = submitted_crt_cnt_dtls[self.file_type]['submitting_header']
            
            line_record = line[0:3]
            line_record_contract = line[0:5]
            
            if line_record == contra_header_record:
                
                if previous_contra_header is not None and previous_contra_header in self.conta_headers_result and \
                "submitted_contract_count_actual" not in self.conta_headers_result[previous_contra_header]:
                    if previous_contra_header in self.conta_headers_result:
                        self.conta_headers_result[previous_contra_header].update({"submitted_contract_count_actual" : contra_header_cnt})
                    else:
                        self.conta_headers_result[previous_contra_header] = {"submitted_contract_count_actual" : contra_header_cnt}
                    contra_header_cnt = 0

                start = submitted_crt_cnt_dtls[self.file_type]['start']
                end =  submitted_crt_cnt_dtls[self.file_type]['end']
                length = submitted_crt_cnt_dtls[self.file_type]['length']
                
                line_submitted_contract_record_count = line[start-1:end]

                if len(line_submitted_contract_record_count.strip()) !=  length:
                    print(f'contra_header_validaton() submitted_contract_count count is missing or Invalid {line_submitted_contract_record_count}')
                    self.subumitted_contract_count_check = False
                else:
                    print(f'contra_header_validaton() submitted_contract_count {line_submitted_contract_record_count} is not missing')
    
                result =  self.subumitted_contract_count_check
                
                if line_submitted_contract_record_count.strip():
                    line_submitted_contract_record_count = int(line_submitted_contract_record_count)
                else:
                    line_submitted_contract_record_count = 0
                
                if line in self.conta_headers_result:
                    self.conta_headers_result[line].update({"submitted_contract_count_present_in_header" : line_submitted_contract_record_count, "submitted_contract_count_present_in_header_validation_result": result})
                else:
                    self.conta_headers_result[line] = {"submitted_contract_count_present_in_header" : line_submitted_contract_record_count, "submitted_contract_count_present_in_header_validation_result": result}
            
                
                start = delivered_crt_cnt_dtls[self.file_type]['start']
                end =  delivered_crt_cnt_dtls[self.file_type]['end']
                length = delivered_crt_cnt_dtls[self.file_type]['length']
                
                line_delivered_contract_record_count = line[start-1:end]

                if len(line_delivered_contract_record_count.strip()) !=  length:
                    print(f'contra_header_validaton() submitted_contract_count count is missing or Invalid {line_delivered_contract_record_count}')
                    self.delivered_contract_count_check = False
                else:
                    print(f'contra_header_validaton() submitted_contract_count {line_delivered_contract_record_count} is not missing')
    
                result =  self.delivered_contract_count_check
                
                if line_delivered_contract_record_count.strip():
                    line_delivered_contract_record_count = int(line_delivered_contract_record_count)
                else:
                    line_delivered_contract_record_count = 0
                
                if line in self.conta_headers_result:
                    self.conta_headers_result[line].update({"delivered_contract_count_present_in_header" : line_delivered_contract_record_count, "delivered_contract_count_present_in_header_validaton_result": result})
                else:
                    self.conta_headers_result[line] = {"delivered_contract_count_present_in_header" : line_delivered_contract_record_count, "delivered_contract_count_present_in_header_validaton_result": result}
            
                previous_contra_header = line
                
            elif line_record_contract == contract_header:
                
                contra_header_cnt += 1
                
                if self.file_type == "COM":
                    start = nscc_control_rec_dtls[self.file_type]['start']
                    end =  nscc_control_rec_dtls[self.file_type]['end']
                    length = nscc_control_rec_dtls[self.file_type]['length']
                    
                    line_nscc_control_number = line[start-1:end]
                    self.nscc_control_number_list.append(line_nscc_control_number.strip())

                    if len(line_nscc_control_number.strip()) !=  length:
                        print(f'contra_header_validaton() NSCC control number is missing or Invalid {line_nscc_control_number}')
                        self.nscc_control_number_check = False
                    else:
                        print(f'contra_header_validaton() NSCC control number {line_nscc_control_number} is not missing')
        
                    result =  self.nscc_control_number_check
                    
                    if previous_contra_header in self.conta_headers_result:
                        self.conta_headers_result[previous_contra_header].update({"nscc_control_number_present_in_header" : line_nscc_control_number, "nscc_control_number_present_in_header_validation_result": result})
                    else:
                        self.conta_headers_result[previous_contra_header] = {"nscc_control_number_present_in_header" : line_nscc_control_number, "nscc_control_number_present_in_header_validation_result": result}
            
            elif self.file_type == 'FAR' and line_record_contract == nscc_control_rec_dtls[self.file_type]['contract']:
                
                start = nscc_control_rec_dtls[self.file_type]['start']
                end =  nscc_control_rec_dtls[self.file_type]['end']
                length = nscc_control_rec_dtls[self.file_type]['length']
                
                line_nscc_control_number = line[start-1:end]
                self.nscc_control_number_list.append(line_nscc_control_number.strip())

                if len(line_nscc_control_number.strip()) !=  length:
                    print(f'contra_header_validaton() NSCC control number is missing or Invalid {line_nscc_control_number}')
                    self.nscc_control_number_check = False
                else:
                    print(f'contra_header_validaton() NSCC control number {line_nscc_control_number} is not missing')
    
                result =  self.nscc_control_number_check
                
                if previous_contra_header in self.conta_headers_result:
                    self.conta_headers_result[previous_contra_header].update({"nscc_control_number_present_in_header" : line_nscc_control_number, "nscc_control_number_present_in_header_validation_result": result})
                else:
                    self.conta_headers_result[previous_contra_header] = {"nscc_control_number_present_in_header" : line_nscc_control_number, "nscc_control_number_present_in_header_validation_result": result}
            
            
            elif line_record == submitting_header:
                if previous_contra_header is not None:
                    if previous_contra_header in self.conta_headers_result:
                        if self.conta_headers_result[previous_contra_header]["submitted_contract_count_present_in_header"] == contra_header_cnt:
                            self.conta_headers_result[previous_contra_header].update({"submitted_contract_actual_count" : contra_header_cnt,
                                                                                      "submitted_contract_final_match_result": True})
                        else:
                            self.conta_headers_result[previous_contra_header].update({"submitted_contract_actual_count" : contra_header_cnt,
                                                                                      "submitted_contract_final_match_result": False})
                    else:
                        if self.conta_headers_result[previous_contra_header]["submitted_contract_count_present_in_header"] == contra_header_cnt:
                            self.conta_headers_result[previous_contra_header] = {"submitted_contract_actual_count" : contra_header_cnt,
                                                                                      "submitted_contract_final_match_result": True}
                        else:
                            self.conta_headers_result[previous_contra_header] = {"submitted_contract_actual_count" : contra_header_cnt,
                                                                                      "submitted_contract_final_match_result": False}
                    contra_header_cnt = 0
            elif line_record == "END":
                if previous_contra_header in self.conta_headers_result:
                    if self.conta_headers_result[previous_contra_header]["submitted_contract_count_present_in_header"] == contra_header_cnt:
                            self.conta_headers_result[previous_contra_header].update({"submitted_contract_actual_count" : contra_header_cnt,
                                                                                      "submitted_contract_final_match_result": True})
                    else:
                        self.conta_headers_result[previous_contra_header].update({"submitted_contract_actual_count" : contra_header_cnt,
                                                                                  "submitted_contract_final_match_result": False})
                else:
                    if self.conta_headers_result[previous_contra_header]["submitted_contract_count_present_in_header"] == contra_header_cnt:
                            self.conta_headers_result[previous_contra_header] = {"submitted_contract_actual_count" : contra_header_cnt,
                                                                                      "submitted_contract_final_match_result": True}
                    else:
                        self.conta_headers_result[previous_contra_header] = {"submitted_contract_actual_count" : contra_header_cnt,
                                                                                  "submitted_contract_final_match_result": False}
        
        
        fp.close()
        
        print("contra_header_validaton() Execution Completed")
    
    def datatrak_rec_count_validation(self, total_rec_count_dtls, line):
        
       
        start = total_rec_count_dtls[self.file_type]['start']
        end =  total_rec_count_dtls[self.file_type]['end']
        length = total_rec_count_dtls[self.file_type]['length']
        
        line_datatrak_rec_count = line[start-1:end]

        if len(line_datatrak_rec_count.strip()) !=  length:
            print(f'participant_number_validation() Datatrak count is missing or Invalid {line_datatrak_rec_count}')
            self.datatrak_count_check = False
        else:
            print(f'participant_number_validation() Datatrak {line_datatrak_rec_count} is not missing')
        
        result = self.datatrak_count_check
        
        if line_datatrak_rec_count.strip():
            line_datatrak_rec_count = int(line_datatrak_rec_count)
        else:
            line_datatrak_rec_count = 0
        
        if line in self.data_trak_header_result:
            self.data_trak_header_result[line].update({"datatrak_rec_count_present_in_file_header" : line_datatrak_rec_count, "datatrak_rec_count_present_in_file_header_validation_result": result})
        else:
            self.data_trak_header_result[line] = {"datatrak_rec_count_present_in_file_header" : line_datatrak_rec_count, "datatrak_rec_count_present_in_file_header_validation_result": result}
    
    def participant_number_validation(self, participant_num_dtls, line):
        
       
        start = participant_num_dtls[self.file_type]['start']
        end =  participant_num_dtls[self.file_type]['end']
        length = participant_num_dtls[self.file_type]['length']
        
        line_participant_number = line[start-1:end]

        if len(line_participant_number.strip()) !=  length:
            print(f'participant_number_validation() Participant number is missing or Invalid {line_participant_number}')
            self.participant_number_check = False
        else:
            print(f'participant_number_validation() Participant number {line_participant_number} is not missing')
        
        result = self.participant_number_check
        
        if line in self.submitting_headers_result:
            self.submitting_headers_result[line].update({"participant_number_present_in_header" : line_participant_number, "participant_number_present_in_header_validation_result": result})
        else:
            self.submitting_headers_result[line] = {"participant_number_present_in_header" : line_participant_number, "participant_number_present_in_header_validation_result": result}
            
    
    def submitting_header_count_validation(self, submitting_header_rec_count_dtls, line):
        
       
        start = submitting_header_rec_count_dtls[self.file_type]['start']
        end =  submitting_header_rec_count_dtls[self.file_type]['end']
        length = submitting_header_rec_count_dtls[self.file_type]['length']
        
        line_submitting_header_count = line[start-1:end]

        if len(line_submitting_header_count.strip()) !=  length:
            print(f'submitting_header_count_validation() Submitting number is missing or Invalid {line_submitting_header_count}')
            self.submitting_header_count_check = False
        else:
            print(f'submitting_header_count_validation() Submitting number {line_submitting_header_count} is not missing')
        
        result = self.submitting_header_count_check

        if line_submitting_header_count.strip():
            line_submitting_header_count = int(line_submitting_header_count)
        else:
            line_submitting_header_count = 0
        
        if line in self.submitting_headers_result:
            self.submitting_headers_result[line].update({"submitting_header_count_present_in_header" : line_submitting_header_count, "submitting_header_count_present_in_header_validation_result": result})
        else:
            self.submitting_headers_result[line] = {"submitting_header_count_present_in_header" : line_submitting_header_count, "submitting_header_count_present_in_header_validation_result": result}
            
    
    def transmission_id_validation(self, transmission_id_rec_dtls, line):
        
        
        start = transmission_id_rec_dtls[self.file_type]['start']
        end =  transmission_id_rec_dtls[self.file_type]['end']
        length = transmission_id_rec_dtls[self.file_type]['length']
        
        line_transmission_id = line[start-1:end-8]
        self.transmission_id_list.append(line_transmission_id.strip())

        if len(line_transmission_id.strip()) !=  length-8:
            print(f'transmission_id_validation() transmission id is missing or Invalid {line_transmission_id}')
            self.transmission_id_check = False
        else:
            print(f'transmission_id_validation() transmission id {line_transmission_id} is not missing')
            
        result = self.transmission_id_check
        
        if line in self.submitting_headers_result:
            self.submitting_headers_result[line].update({"transmission_id_present_in_header" : line_transmission_id, "transmission_id_present_in_header_validation_result": result})
        else:
            self.submitting_headers_result[line] = {"transmission_id_present_in_header" : line_transmission_id, "transmission_id_present_in_header_validation_result": result}
    
    
    def ips_business_code_validation(self, ips_business_code_rec_dtls, line):
        
        start = ips_business_code_rec_dtls[self.file_type]['start']
        end =  ips_business_code_rec_dtls[self.file_type]['end']
        valid_ips_business_code = ips_business_code_rec_dtls[self.file_type]['value']
        length = ips_business_code_rec_dtls[self.file_type]['length']
        
        line_ips_business_code = line[start-1:end]

        if len(line_ips_business_code.strip()) !=  length or line_ips_business_code != valid_ips_business_code:
            print(f'ips_business_code_validation() IPS business code is missing or invalid  {line_ips_business_code}')
            self.ips_business_code_check = False
        else:
            print(f'ips_business_code_validation() IPS business code {line_ips_business_code} is not missing')
            
        result = self.ips_business_code_check
        
        if line in self.submitting_headers_result:
            self.submitting_headers_result[line].update({"ips_business_code_id_present_in_header" : line_ips_business_code, "ips_business_code_id_present_in_header_validation_result": result})
        else:
            self.submitting_headers_result[line] = {"ips_business_code_id_present_in_header" : line_ips_business_code, "ips_business_code_id_present_in_header_validation_result": result}
                
    
    def ips_indicator_validation(self, ips_indicator_rec_dtls, line):
        
        start = ips_indicator_rec_dtls[self.file_type]['start']
        end =  ips_indicator_rec_dtls[self.file_type]['end']
        valid_ips_business_ind = ips_indicator_rec_dtls[self.file_type]['value']
        length = ips_indicator_rec_dtls[self.file_type]['length']
        
        line_ips_ind = line[start-1:end]

        if len(line_ips_ind.strip()) !=  length or line_ips_ind not in valid_ips_business_ind:
            print(f'ips_indicator_validation() IPS indicator is missing or invalid  {line_ips_ind}')
            self.ips_ind_check = False
        else:
            print(f'ips_indicator_validation() IPS indicator {line_ips_ind} is not missing')
            
        result = self.ips_ind_check
        
        if line in self.submitting_headers_result:
            self.submitting_headers_result[line].update({"ips_ind_id_present_in_header" : line_ips_ind, "ips_ind_id_present_in_header_validation_result": result})
        else:
            self.submitting_headers_result[line] = {"ips_ind_id_present_in_header" : line_ips_ind, "ips_ind_id_present_in_header_validation_result": result}
        
    
    def submitting_header_validation(self, file_path):
        
        print("submitting_header_validation() Execution Started")

        participant_num_dtls =  {'COM' : {'start': 4, 'end': 7, 'length' : 4, 'record': 'C20'},
                                 'POV' : {'start': 4, 'end': 7, 'length' : 4, 'record': 'C10'},
                                 'FAR' : {'start': 87, 'end': 90, 'length' : 4, 'record': 'C40'}}
                            
        
        transmission_id_rec_dtls =  {'COM' : {'start': 11, 'end': 40, 'length' : 30, 'record': 'C20'},
                                     'POV' : {'start': 11, 'end': 40, 'length' : 30, 'record': 'C10'},
                                     'FAR' : {'start': 4, 'end': 33, 'length' : 30, 'record': 'C40'}
                                    }
        
        ips_business_code_rec_dtls =  {'COM' : {'start': 8, 'end': 10, 'length' : 3, 'record': 'C20', 'value': 'COM'},
                                       'POV' : {'start': 8, 'end': 10, 'length' : 3, 'record': 'C10', 'value': 'POV'},
                                       'FAR' : {'start': 171, 'end': 173, 'length' : 3, 'record': 'C40', 'value': 'FAR'}
                                      }
        
        ips_indicator_rec_dtls =  {'COM' : {'start': 53, 'end': 53, 'length' : 1, 'record': 'C20', 'value': ['T', 'P']},
                                       'POV' : {'start': 61, 'end': 61, 'length' : 1, 'record': 'C10', 'value': ['T', 'P']},
                                       'FAR' : {'start': 186, 'end': 186, 'length' : 1, 'record': 'C40', 'value': ['T', 'P']}
                                      }
        
        submitting_header_rec_count_dtls =  {'COM' : {'start': 41, 'end': 52, 'length' : 12, 'record': 'C20'},
                                         'POV' : {'start': 41, 'end': 52, 'length' : 12, 'record': 'C10'},
                                         'FAR' : {'start': 174, 'end': 185, 'length' : 12, 'record': 'C40'}}
        
        total_rec_count_dtls =  {'COM' : {'start': 27, 'end': 33, 'length' : 7, 'record': 'C20'},
                                 'POV' : {'start': 27, 'end': 33, 'length' : 7, 'record': 'C10'},
                                 'FAR' : {'start': 27, 'end': 33, 'length' : 7, 'record': 'C40'}}
                
        fp = open(file_path)
        
        submitting_header_line_count = 0
        submitting_line = None
        total_line_count = 0
            
        for line in fp:
            
            total_line_count += 1
            if line[0:3] == "HDR":
                continue

            line_record = line[0:3]
            submitting_record = participant_num_dtls[self.file_type]['record']

            self.participant_number_check = True
            self.transmission_id_check = True
            self.ips_business_code_check = True
            self.ips_ind_check = True
            self.submitting_header_count_check = True
            
            submitting_header_line_count += 1
            
            if line_record == submitting_record:
                self.participant_number_validation(participant_num_dtls, line)
                self.transmission_id_validation(transmission_id_rec_dtls, line)
                self.ips_business_code_validation(ips_business_code_rec_dtls, line)
                self.ips_indicator_validation(ips_indicator_rec_dtls, line)
                self.submitting_header_count_validation(submitting_header_rec_count_dtls, line)
                if submitting_header_line_count > 1:
                    submitting_header_line_count -= 1
                    if submitting_line in self.submitting_headers_result:
                        self.submitting_headers_result[submitting_line].update({"submitting_header_actual_count" : submitting_header_line_count})
                submitting_line =  line
                submitting_header_line_count = 1
            elif line_record == "END":
                submitting_header_line_count -= 1
                if submitting_line in self.submitting_headers_result:
                    self.submitting_headers_result[submitting_line].update({"submitting_header_actual_count" : submitting_header_line_count})
                self.datatrak_rec_count_validation(total_rec_count_dtls, line)
                
                if self.data_trak_header_result[line]["datatrak_rec_count_present_in_file_header"] == total_line_count:
                    self.data_trak_header_result[line].update({"datatrak_actual_rec_count" : total_line_count, "datatrak_compare_result" : True})
                else:
                    self.data_trak_header_result[line].update({"datatrak_actual_rec_count" : total_line_count, "datatrak_compare_result" : False})


        fp.close()
        
        for key, rec in self.submitting_headers_result.items():
            if rec['submitting_header_actual_count'] == rec['submitting_header_count_present_in_header']:
                self.submitting_headers_result[key].update({"submitting_header_count_final_match_result" : True})
            else:
                self.submitting_headers_result[key].update({"submitting_header_count_final_match_result" : False})
                
        print("submitting_header_validation() Execution Completed")
        


dtcc_validation_obj = DtccValidation()
