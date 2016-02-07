from math import log
import random
import matplotlib.pyplot as plt

import matplotlib as mpl
import numpy as np

import mpl_toolkits.mplot3d.art3d as art3d

def KLM_executiontime (categories, subcategories ,p_error, scrolling,hc1,hc2):

        tm = 1.25 #mental act
        tr = 0.05 #system response time

        #categories selection definition -> 2 and 4
        category1 = 2
        pc1 = 0.2
        #hc1 = 22
        category2 = 4
        pc2 = 0.15
        #hc2 = 18
        hc_next = 22
        
        #subcategories selection defintion -> 2 and 6
        subcategory2 = 4
        psc2 = 0.30
        subcategory6 = 6
        psc6 = 0.10


        #estimated time for categories in main meny
        t_categories = SDP_selectiontime (0,categories, category1, pc1*history_length, pc1,hc1) + SDP_selectiontime (0,categories, category2, pc2*history_length, pc2,hc2)
        t_next = SDP_selectiontime (0,categories, categories, pc1*history_length, pc1,hc_next)

        #estimated time for subcategories in submenu
        t_subcategories_hc1 = SDP_selectiontime (scrolling,subcategories, subcategory6, psc6*history_length, psc6,hc1) + SDP_selectiontime (scrolling,subcategories, subcategory2, psc2*history_length, psc2,hc1)
        t_subcategories_hc2 = SDP_selectiontime (scrolling,subcategories, subcategory6, psc6*history_length, psc6,hc2) + SDP_selectiontime (scrolling,subcategories, subcategory2, psc2*history_length, psc2,hc2)


        t_ok = 2*(tm + t_categories + t_next + 4*tr) + t_subcategories_hc1 + t_subcategories_hc2
        t_error = t_ok + tm + t_next + t_subcategories_hc1

        t = (1 - p_error)*t_ok + p_error * t_error
        
        return t
        

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
        t_pi = a_pi + b_pi * log((item_height * itemposition + 1))
        
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
y_axis = []
z1_axis = []
z2_axis = []
z3_axis = []
z4_axis = []
z5_axis = []
z6_axis = []
history_length = 1000

sc = [[0 for x in range(4)] for x in range(4)]
vector_c1 = []
optimal = 9999999999999999999999999999999999999999
#KLM_executiontime (categories, subcategories ,p_error, scrolling)
for i in range(4):
        #categories i from 4 to 6
        for j in range(4):
                #subcategories j from 5 to 8       
                category = i + 4
                subcategory = j + 5
                
                x_axis.append(i+4)
                y_axis.append(j+5)
                
                z1_axis.append(KLM_executiontime (category, subcategory,0.3, 0,16,16))
                z2_axis.append(KLM_executiontime (category, subcategory ,0.3, 1,16,16))
                z3_axis.append(KLM_executiontime (category, subcategory ,0.3, 0,24,24))
                z4_axis.append(KLM_executiontime (category, subcategory ,0.3, 1,24,24))
                z5_axis.append(KLM_executiontime (category, subcategory ,0.3, 0,16,24))
                z6_axis.append(KLM_executiontime (category, subcategory ,0.3, 1,24,16))
                
                if KLM_executiontime (category, subcategory ,0.3, 0,16,16) < optimal :
                        optimal = KLM_executiontime (category, subcategory ,0.3, 0,16,16)
                        i_ = category
                        j_ = subcategory
                        scrolling_=0
                if KLM_executiontime (category, subcategory ,0.3, 1,16,16) < optimal :
                        optimal = KLM_executiontime (category, subcategory ,0.3, 1,16,16)
                        i_ = category
                        j_ = subcategory
                        scrolling_=1
                 

print("optimal ->",optimal)
print("number of categories ->",i_)
print("number of subcategories ->",j_)
print("scrolling ?->",scrolling_)

fig = plt.figure()
ax = fig.gca(projection='3d')
z = np.linspace(-2, 2, 100)

ax.plot(x_axis, y_axis, z1_axis,'yo', label='no-scro,16p')
ax.plot(x_axis, y_axis, z2_axis,'bo', label='scro,16p')
ax.plot(x_axis, y_axis, z3_axis,'go', label='no-scro,24p')
ax.plot(x_axis, y_axis, z4_axis,'ro', label='scro,24p')
ax.plot(x_axis, y_axis, z5_axis,'ko', label='no-scro,16v24p')
ax.plot(x_axis, y_axis, z6_axis,'mo', label='scro,24v16p')
ax.legend()
fig.suptitle('Estimated KLM times')
plt.xlabel('Number of categories')
plt.ylabel('Number of subcategories')

plt.show()




        


        



