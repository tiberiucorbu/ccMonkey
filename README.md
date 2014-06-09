# CCMonkey

Cruise Controll Monkey, is a software component designed for RasperryPi, it's aim is to notify build failure for a selection of projects. Works toghether with jenkins cruise controll standard that provides an xml which contains build status for all the jobs in a particular view.

This piece of software retrieves this cc.xml file from jenkins, parses it, filters out the projects that are not of intrest and decides depending on a state Ex: "Build failure" to alarm the Monkey by lighting up one of the RaspberryPI GPIO pin.  

## The monkey 

The monkey is a stuffed toy that cries if you steal it's banana, the electric circuit was interfaced with a rellay on the "Cry" trigger switch. Doing so, small requirements ware needed to make the monkey cry from the software side, provide a current to the input of the rellay block and the monkey would cry.   


