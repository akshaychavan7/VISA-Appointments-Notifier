# VISA-Appointments-Notifier
A python script to check for visa appointments availability and notify you accordingly. 


## How to run this script - 
1. Get your sender email ID's password using two-step verification. (Follow this tutorial)
2. Add the Sender Email, Sender Email's Password, and Receiver Email in this script
3. Update the visa_notifier.bat file given in this folder as per your script's path
4. Create a Windows Scheduler Task, so that it will continuously run this script using following steps - <br/>
    i. Search task scheduler in your windows search menu <br/>
    ii. Actions ==> Create task ==> give the name you want for this task <br/>
    iii. Open Triggers tab ==> Select Daily ==> select start date and time as per your current date ==> recur every 1 days ==> Check repeat task every option and select option as 5 minutes ==> OK <br/>
    iv. Open Actions tab ==> New ==> Click on browse ==> Select the visa_notifier.bat file that we have created ==> OK <br/>
    v. To test this task ==> right click on the task that you've just created ==> run ==> it will open a command promt window ==> check for the output there <br/>
5. Check each day if your script is running or not, this is to avoid any failures.<br/>

##
© Akshay Chavan
