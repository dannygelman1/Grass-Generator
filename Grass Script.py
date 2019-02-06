#grassScript.py
import maya.cmds as cmds
import random
import functools

def createUI(pWindowTitle, pApplyCallback):
    '''
    This is a function that creates the user interface, where users can input the x and z coordinate range
    where they want grass to generate, the number of blades to generate, and how tall on average they want 
    their grass to be
    '''
    
    windowID = 'Grass'
    
    if cmds.window(windowID, exists=True):
        cmds.deleteUI(windowID)
    #creating UI window  
    cmds.window(windowID, title = pWindowTitle, sizeable=True, resizeToFitChildren=True)
    cmds.rowColumnLayout(numberOfColumns=3, columnWidth=[(1,130), (2,60), (3,60)], columnOffset = [(1,'right',3)])
    
    #creating input fields in UI window
    cmds.text(label='X Range: ')
    XSpaceLowerInput = cmds.intField()
    XSpaceUpperInput = cmds.intField()
    cmds.text(label='Z Range: ')
    ZSpaceLowerInput = cmds.intField()
    ZSpaceUpperInput = cmds.intField()
    cmds.text(label='Number Grass Blades: ')
    NumBladesInput = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.text(label='Approximate' + '\n' + 'Average Height: ')
    AvgHeightInput = cmds.intField()
    cmds.separator(h=10,style='none')
    cmds.separator(h=10,style='none')
    cmds.separator(h=10,style='none')
    cmds.separator(h=10,style='none')
    cmds.separator(h=10,style='none')
    
    #making the apply button call the applyCallback
    cmds.button(label='Apply', command=functools.partial(pApplyCallback, NumBladesInput, XSpaceLowerInput,
                                                XSpaceUpperInput, ZSpaceLowerInput, ZSpaceUpperInput, AvgHeightInput))
    def cancelCallback(*pArgs):
        if cmds.window(windowID, exists=True):
            cmds.deleteUI(windowID)
    cmds.button(label='Cancel', command=cancelCallback)
    cmds.showWindow()
    
def applyCallback(pNumberBlades, pXSpaceLower, pXSpaceUpper, pZSpaceLower, pZSpaceUpper, pAverageHeight, *pArgs):
    '''
    This function generates the grass using the inputs from the user.
    '''
    random.seed(100)  

    #creating initial blade of grass
    startR = 0.1
    startH = 1
    result = cmds.polyCone(r=startR, h=startH, name ='OGCone#')
    coneGroup = cmds.group(empty = True, name ="coneGroup")
     
    #retreiveing data inputed by user
    XSpaceLower =  cmds.intField(pXSpaceLower, query=True,value = True)
    XSpaceUpper = cmds.intField(pXSpaceUpper, query=True,value = True)
    ZSpaceLower =  cmds.intField(pZSpaceLower, query=True,value = True)
    ZSpaceUpper =  cmds.intField(pZSpaceUpper, query=True,value = True)
    NumberBlades =  cmds.intField(pNumberBlades, query=True,value = True)
    AverageHeight =  cmds.intField(pAverageHeight, query=True,value = True)
    
    #generating grass based on user inputs
    for i in range(0,int(NumberBlades)):
        x=random.uniform(XSpaceLower,XSpaceUpper)
        z=random.uniform(ZSpaceLower,ZSpaceUpper)
        #scaling each blade to have slight variations in radii and height
        randR=random.uniform(0.05,0.3)
        randY=random.uniform(0.8, 1.1)
        resInstance = cmds.instance(result[0], name = 'cone#')
        cmds.scale(randR, randY * AverageHeight, randR, resInstance)
        #moving all the blades up so that they are bottom aligned with the xz plane
        moveToOriginY = (startH * randY * AverageHeight)/2
        cmds.move(x,moveToOriginY,z, resInstance)
        cmds.parent(resInstance, coneGroup)
    
    #hiding the initial blade
    cmds.hide(result)
    cmds.xform(coneGroup, centerPivots = True)
    
createUI ('Grass Input', applyCallback)
 
    
