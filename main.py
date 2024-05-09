'''
L-System Interpreter
Author: Karina Cabrera

TODO:
Apply rotation to X and Y axis (Shear mapping)
Create a method to find ends of branches
Create a method for blender interpretation (I want to use blender curves to interpret stems and stem branches)

How it works:
The Axiom class is used to create a rule
After rules are created apply to list
L_SYS takes the Rule List aswell as iterations, angle and first rule and creates a string based on those rules

'''
class Axiom(object):
    # Used to create rules
    def __init__(self, name, rule):
        self.name = name
        self.rule = rule

    def rulestolist(self):
        rulelist = []
        for i, v in enumerate(self.rule):
            rulelist.append(v)
        return rulelist

    def to_string(self):
        print(self.name, ': ', self.rule)
class L_SYS(object):

    def __init__(self, StartingRule, Iterations, angle, Rule_List):
        self.StartingRule = StartingRule
        self.Iterations = Iterations
        self.angle = angle
        self.Rule_List = Rule_List

    def convertToGrammer(self, i, n, myList):
        if n == 0:
            myList.append(i.name)
            return i
        else:
            rulelist = i.rulestolist()
            for i in range(len(rulelist)):
                if self.getaxiomrules(rulelist[i]) == False:
                    myList.append(rulelist[i])
                else:
                    X = self.getaxiomrules(rulelist[i])
                    self.convertToGrammer(X, n - 1, myList)

    # TODO: finish method
    def ExpandString(self):
        # TODO: Reverse Factorizaiton for easy reading of L System's string
        # Ex: F+(+F-X) --> F(++F+-X)
        grammerlist = self.getGrammerList()
        current_effect = []
        Temporary_list = []
        for i in range(len(grammerlist)):

            if (grammerlist[i] == '+' and grammerlist[i + 1] == '[') or (
                    grammerlist[i] == '-' and grammerlist[i + 1] == '['):
                current_effect.append(grammerlist[i])
            elif (grammerlist[i] == '+' and grammerlist[i + 1] is not None) or (
                    grammerlist[i] == '-' and grammerlist[i + 1] is not None):
                Temporary_list.append(grammerlist[i])
            elif grammerlist[i] == '[':
                Temporary_list.append(grammerlist[i])

            else:
                Temporary_list.append(grammerlist[i])

        return (Temporary_list)

    def readString(self):
        # TODO: apply rotation to x and y for usage in 3d software
        grammerlist = self.getGrammerList()
        current_y_local = 0
        current_x_local = 0
        current_Z_rot = 0
        OGX = []
        OGR = []

        print('String Generated from Grammer: ', grammerlist)
        for i in range(len(grammerlist)):
            if grammerlist[i] == '[':
                current_y_local = current_y_local + 1

            elif grammerlist[i] == '+':
                current_x_local = current_x_local + 1
                current_Z_rot = current_Z_rot + self.angle

            elif grammerlist[i] == '-':
                current_x_local = current_x_local - 1
                current_Z_rot = current_Z_rot - self.angle

            elif grammerlist[i] == ']':
                OGX.pop()
                current_x_local = OGX[-1]
                OGR.pop()
                current_Z_rot = OGR[-1]
                current_y_local = current_y_local - 1

            if grammerlist[i].isalpha():
                OGX.append(current_x_local)
                OGR.append(current_Z_rot)

                print('Stem', grammerlist[i], ':', '\nY location: ', current_y_local, '\nX Location: ',
                      current_x_local, '\nRotation: ', current_Z_rot, '\n')

    def getGrammerList(self):
        templist = []
        self.convertToGrammer(self.StartingRule, self.Iterations, templist)
        return templist

    def printallrules(self):
        print('Axioms and Rules: ')
        for i in self.Rule_List:
            i.to_string()

    def getaxiomrules(self, name):
        # gets a variables name and checks if it has a linked rule
        for i in self.Rule_List:
            if name == i.name:
                return i
        return False

##########
#EXAMPLES#
#########

# Rules Take from The Algorithmic Beauty of plants
rule1 = Axiom('b', 'a')
rule2 = Axiom('a', 'ab')
Rule_list1 = [rule1, rule2]
Test_L_SYS = L_SYS(rule1, 5, 2, Rule_list1)
Test_L_SYS.readString()

'''
NOTE: generates a really long string
plant1 = Axiom('X', 'F-[[X]+X]+F[+FX]-X')
plant2 = Axiom('F', 'FF')
Rule_list2 = [plant1, plant2]
Test_L_SYS = L_SYS(plant1, 5, 22.5, Rule_list2)
Test_L_SYS.readString()
'''

plant1 = Axiom('X', 'F[-X][+X]')
Rule_list3 = [plant1]
Test_L_SYS = L_SYS(plant1, 2, 30, Rule_list3)
Test_L_SYS.readString()

# Note: Blender testing does not currently work, due to how rotation is applied, need to fix:  bpy.ops.mesh.primitive_cube_add(scale = (.5,.5,.5),rotation = (0,0,current_Z_rot),location=(current_x_local, current_y_local, 0))
