from math import log
import random
import matplotlib.pyplot as plt

# Returns the prediction of the SDP model for a given item in a given menu with a given selection history
def SDP_selectiontime (scrolling,menulength, itemposition, trials, p_i,item_height):
        # menulength = the number of items in the menu
        # itemposition = position of the to-be-clicked target item in the menu (1 = first)
        # trials = total number of previous repetitions the user has carried out with this menu
        # probability of this item in the selection history (see slides / paper)

        #item_height = 22                # 22 in pixels 
        #L = 1                         # L=1 means static, immutable menus
        L = 1 # very easy to learn interface    

        if scrolling == 0:
        # expert user - logaritmic on distance (ballistic) - aphabetical order - non scrolling
                #a_pi = -0.17
                a_pi = 0
                b_pi = 0.44

        else:
        # expert user - logaritmic on distance (ballistic) - aphabetical order and scrolling
                #a_pi = -5.13
                a_pi = 0
                b_pi = 1.28
        
        #t_pi = a_pi + b_pi * log((item_height * itemposition)/item_height+1,2)
        t_pi = a_pi + b_pi * log((item_height * itemposition))
        
        #Hi = log(1/p_i,2)
        #b_hh = 0.08
        #a_hh = 0.24
        #t_hhi = b_hh * Hi + a_hh
                
        if scrolling == 0:
        # novice user - random order of items -  time is liniar on distance - non scrolling
                #a_vs = 0.43
                a_vs = 0
                b_vs = 0.12
        else:
        # novice user - random order of items -  time is liniar on distance - non scrolling
                #a_vs = -2.4
                a_vs = 0
                b_vs = 0.19
        
        t_vsi =  a_vs + b_vs * menulength

        #total time - menu performance model that interpolates between novice (liniar) and expert (logaritmic)
        e_i = L * (1-1/trials) # experience with each item at each level
        t_dsi = (1 - e_i) * t_vsi + e_i * t_pi 
        return t_dsi + t_pi

#SDP for all menu items is copied to e
def calc_e (scrolling,menu_lenght,prob,item_height):
        global history_length
        e = []
        for i in range(menu_lenght):
                e.append(SDP_selectiontime(scrolling,menu_lenght,i+1,prob[i]*history_length,prob[i],item_height))
        return e
        #print("INFO : SPD values for menu times ->",e)

#total c for a given menu design
def calc_c (menu_lenght,prob, e):
        global history_length
        c = 0
        for i in range(menu_lenght):
                c = c + ( prob[i] * history_length * e[i] )
        #print("SHOW TOTAL C : ->",c)
        return c

def show_c (menu_lenght,prob, e):
        #total c for a given menu design
        global history_length
        c = []
        for i in range(menu_lenght):
                c.append( prob[i] * history_length * e[i] )
        print("SHOW VECTOR C : ->",c)

#build prob vector with new lenght
def resize_menu(menu_lenght,prob):
        
        global history_length
        prob = []
        if menu_lenght < 15:
                aux = 0
                for i in range(15 - menu_lenght):
                        aux = aux + prob_original[14-i]

                aux = aux / (15 - (15 - menu_lenght))
                for i in range(menu_lenght):
                        prob.append(prob_original[i] + aux)
        else:
                prob = prob_original
        aux = 0
        for i in range(menu_lenght):
                aux = aux + prob[i]
        #print("INFO NEW prob vector >",aux,prob)
        return prob
        
        
# main
menu_lenght = 15
# initialization of designs
design = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]  
# initialization of max to min design
prob_original =[0.16, 0.13,0.12,0.10,0.08,0.07,0.06,0.06,0.05,0.04,0.04,0.03,0.03,0.02,0.01]       
print("max to min design->",design)
print("max to min design prob->",prob_original)
print("-------------------------")
# op
x_axis = []

# no difference between subcategories
sc = []
history_length = 1000

sc = []
vector_c1 = []       
for i in range(menu_lenght-5):
        lenght = i+3
        sc = resize_menu(lenght,prob_original)
        vector_c1.append(calc_c (lenght,sc,calc_e(0,lenght,sc,22)))
        x_axis.append(lenght);

sc = []
vector_c2 = []       
for i in range(menu_lenght-5):
        lenght = i+3
        sc = resize_menu(lenght,prob_original)
        vector_c2.append(calc_c (lenght,sc,calc_e(1,lenght,sc,22)))

sc = []
vector_c3 = []       
for i in range(menu_lenght-5):
        lenght = i+3
        sc = resize_menu(lenght,prob_original)
        vector_c3.append(calc_c (lenght,sc,calc_e(0,lenght,sc,32)))

sc = []
vector_c4 = []       
for i in range(menu_lenght-5):
        lenght = i+3
        sc = resize_menu(lenght,prob_original)
        vector_c4.append(calc_c (lenght,sc,calc_e(1,lenght,sc,32)))

plt.plot(x_axis, vector_c1, 'r-', label="nscr/22p")
plt.plot(x_axis, vector_c3, 'y-', label="nscr/26p")
plt.plot(x_axis, vector_c2, 'b-', label="scr/22p")
plt.plot(x_axis, vector_c4, 'g-', label="scr/26p")
plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
plt.xlabel('Number of displayed subcategories')
plt.ylabel('Total SDP time')
plt.title('Layout characterization')
plt.show()




        


        



