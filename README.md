# Crypto-and-Stock-ML-model
to the moon

### TO CREATE A TWITTER DEVELOPER ACCOUNT:
1. [Create a Twitter account](https://twitter.com).  You can use an existing account if you have one.
2. Under account settings, add your phone number to the account.
3. [Create a Twitter developer account](https://dev.twitter.com/resources/signup).  Attach it to your Twitter account.  You should indicate that you are a student and this is to be used for educational purposes (you can mention the class name), that you are not downloading or processing data in bulk.   
4. Once you're logged into your developer account, [create an application for this assignment](https://apps.twitter.com/app/new).  You can call it whatever you want, and you can write any URL when it asks for a web site.
5. On the page for that application, find your Consumer Key and Consumer Secret.
6. On the same page, create an Access Token.  Record the resulting Access Token and Access Token Secret.
7. Edit the file `keys.json` and replace the placeholders with your keys.

### IMPORTANT NOTE ON API KEYS.
If someone has your authentication keys, they can access your Twitter account and post as you!  So don't give them to anyone, and ###do not commit them to this repository###.  The usual way to store sensitive information like this is to put it in a separate file and read it programmatically.  That way, you can share the rest of your code without sharing your keys. 

### IMPORTANT NOTE ON REQUESTING DATA.
Twitter limits developers to a certain rate of requests for data.  If you make too many requests in a short period of time, you'll have to wait awhile (around 15 minutes) before you can make more.  So carefully follow the code examples you see and don't rerun cells without thinking.  Instead, always save the data you've collected to a file.  You are provided templates to help you do that.
