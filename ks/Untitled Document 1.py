        for a_line in pageTxt:                     
            if(state_machine == 100): 
                if(page == 0):
                    if('Case' in a_line):
                        state_machine = 150  
                else:
                    if ('Change' in a_line):
                        state_machine = 150  
            elif(state_machine == 150): 
                if (page == 0):
                    if('Count' in a_line):
                        state_machine = 200   
                    elif('ount' in a_line):
                        state_machine = 200  
                else:
                    if ('202' in a_line):
                        state_machine = 200     
            elif(state_machine == 200): 
                a_line2 = a_line.split(' ')  
                a_line1 = []  
                print('lllllllllll  ', a_line)   
                if a_line2[0] != '':
                    continue
                if a_line2[0].isalpha() == True:
                    a_name = a_line2[0]
                elif a_line2[0].isdigit() or a_line2.isdigit() == True:
                    if len(a_line2) == 5:
                        case_total_rd = a_line2
                    else:
                        a_number = a_line2
                        case_total_append += int(a_number)
                lst_cases.append([a_name, a_number, 0])

               