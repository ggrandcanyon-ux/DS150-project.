# DS150-project.[README.md](https://github.com/user-attachments/files/24248984/README.md)
# NFL Play Predictor 

A Python file that takes multiple inputs from an NFL game and returns one of the two main play types that the offense is more likely to call in that scenario.  

### How it Works

Our code operates based on team tendencies as well as league averages. Each team is given a Run Ratio and a Pass Ratio based on their playcalls throughout the year, which is the default score that is altered by the inputs. For example, if the Arizona Cardinals passed much more than they ran in 2024, their pass score would start out higher than their run score. But if the input play was a 3rd & 1, they are almost certain to run the ball, so the Run score would overpower this pass bias. 

Based on this score, it then considers the inputs. There are 5 inputs in our code:
- Which team is playing offense
- Which down it is
- Distance to the goal line
- Where the line of scrimmage is on the field
- How much time is left in the quarter
These 5 inputs each have different weighted scores and considerations in the code which uses them to help it determine the call.
### How to Use It
Before you run the file, you must ensure it is in a folder with the "2024_plays.csv", or it will not be able to retrieve the run and pass ratios. When you first run the code, it should return the message "This program predicts the next play (Run or Pass) based on 2024 NFL data." It will then begin to ask for inputs. As an example for how to use the code, I will be describing Josh Jacobs touchdown rush from the video that was used in the slideshow.
#### Team
Here you enter the name of the team that is playing on offense. It is formatted as "Place"+" "+"Team Name", which is the most common way that teams are referred to. In our example, the team playing is the Packers, and they are from Green Bay. For correct formatting, we would input "Green Bay Packers".
#### Down
Here you enter an integer between 1 and 4 for the down. For this, we can look at the score bug and see which down it is. In our example, the score bug says "1st & Goal", so we will input "1".
#### Distance
This is how far the line of scrimmage is from the first down marker. This one is also easy, as the scorebug will always show how far that is (1st & 10, 2nd & 5, etc.), unless they are to the goal line like in our example. For those cases, you can either count the hashes to the end zone or subtract the field position from 100. In our example, There is only 1 hash, so they are on the 1 yard line, and we input "1". We could also do 100 - 99, as that is our field position.
#### Field Position
This is the most complicated one to enter. You have to use the hashes and numbers to determine where the line of scrimmage is (the white line where the offense starts). In our code, 0 is the offense's own end zone, and 100 is the end zone they are trying to get to. From their end zone to the 50, it counts up, so we can rely on these until then. Once they get to the other side, it counts down, and we have to do some mental math. Say the offense is on the other teams 34 yard line. We can subtract this from 100 to get 66, which would be correct. As I said in our example, the Packers are on the 99 yard line, as they are just 1 yard from the end zone, so we input "99".
#### Time Left
Finally, we just look back to the score bug and input how much time is left. It works with floats if you want to be precise, but the line it is looking for is 2 minutes. Past the 2 minute warning is when most teams enter hurry up offense and when this input actually matters. In our example, there is 5 minutes and 38 seconds left, so "5.6" will suffice.
### Returns
The program will then return everything you inputted in case you made a mistake. After that, it says its prediction, followed by two calculated run and pass scores. The prediction returned is the higher of those two scores. If the scores are equal, it will return run, as most NFL teams will take a reliable run when possible. In our example, it returned a run. This was correct, as Josh Jacobs rushed for a 1 yard touchdown on the play.
