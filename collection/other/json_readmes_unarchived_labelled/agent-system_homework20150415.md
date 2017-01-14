# homework20150415
homeworks for agent system

1. Create your github account
2. Set your profile
3. Register your information to google docs (**Due. 04/23**)
  https://docs.google.com/spreadsheets/d/1GaMI16ITUWpYn3JHbWIZvhtHnBBcHC33f4WcgMq5VuE/edit?usp=sharing
4. Setup ROS / Euslisp on your PC
  - for Ubuntu 12.04
  ```
sudo sh -c 'echo "deb http://packages.ros.org/ros-shadow-fixed/ubuntu precise main" > /etc/apt/sources.list.d/ros-latest.list'
wget https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install ros-hydro-roseus
# you may have to reboot
echo "source /opt/ros/hydro/setup.bash" >> ~/.bashrc
source ~/.bashrc
rosrun euslisp irteusgl
```
  - for Ubuntu 12.10 and above
  ```
sudo sh -c 'echo "deb http://packages.ros.org/ros-shadow-fixed/ubuntu `lsb_release -cs` main" > /etc/apt/sources.list.d/ros-latest.list'
wget https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -O - | sudo apt-key add -
sudo apt-get update
sudo apt-get install ros-indigo-roseus
# you may have to reboot
echo "source /opt/ros/indigo/setup.bash" >> ~/.bashrc
source ~/.bashrc
rosrun euslisp irteusgl
```
6. Execute on `irteusgl` below:

  ```lisp
(load "irteus/demo/demo.l")
(hand-grasp) ;; or (particle)
```
7. Take screenshot of the `IRTViewer` window
8. Fork this(`agent-system/homework20150415`) repository
9. Clone forked repository to your workspace on local machine (e.g.: `/home/<your account>/agentsystem`)

  ```
cd /home/<your account>/agentsystem
git clone https://github.com/<your user name>/homework20150415
cd homework20150415
```
10. Checkout a branch to push

  ```
git checkout -b my-first-homework
```
11. Copy the screenshot to this directory

  ```
cp <screenshot directory>/screenshotXXX.png ./<your student id>.png
```
12. Commit your change

  ```
git add <your student id>.png
git commit -m "add my awesome screenshot"
```
13. Push your change to github

  ```
git push origin my-first-homework
```
14. Create Pull-request to `agent-system/homework20150415`
