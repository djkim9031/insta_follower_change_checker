# insta_follower_change_checker
First personal project on selenium


As it is my first personal project on selenium - the codes are pretty simple and straightforward.

Basically you just input your Instagram username and password as string values, and in order to initialize you first execute the following commands,

myAccount.fetch_followers()
myAccount.save()

This fetches your current followers and save the number of your followers and follower account names in .txt format 
.txt format is "followers_on_DD_MM_YYYY.txt"

Then after a few days, if you have noticed some changes to your follower numbers or something, run 
myAccount.fetch_followers()
myAccount.follower_change()
myAccount.save()

In the follower_change() method, you have to manually designate the text file path/name against which you will compare your current followers.



!!As most websites change their xpath frequently, this may not run in the future.
It is relevant at the time of writing (July 2nd 2020)


!!Again, it is simply for my personal project
