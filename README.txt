Welcome, and enjoy, to Doge Inc's FIRST RELEASE: Wow-1.0
We hope you will find pleasure in the small things, and
appreciation of the large (nothing's large, it's all small),
but whatever you take away from this, we will help you get started.

First of all, there are no extra apps or plugins to install, and
there are a few users registered on the system already for your browsing
pleasure. They belong to the zipcode 12345 and 54321, if you feel like
creating a new user to share with them. All passwords are "Password",
and the site navigation should be mostly self-explanatory.

Once you start up the server by clicking the server.bat file provided if you're on Windows 
("python manage.py runserver" in the terminal on any other operating system), and go to the
browser URL, you will find yourself on the main page, and you can log-in
in the top right or register. If you try to go anywhere else without logging in, you
will most likely (hopefully) be redirected back to this page.

Once you've logged in you have a few options in the navigation on the top right:
1: Manage account
	This will take you to a page where you can update your information. At the
	moment, since we're still unused to how forms work and need a little bit more
	experience, this will allow you to edit absolutely anything of your user's db
	table. The assumption is that since you're logged in, you know your password,
	and as such, any password you enter, so long as both fields are the same,
	will update everything to what you've entered on the page. You should be able
	to change your zipcode without a problem (we haven't implemented warnings yet),
	but only to a 5 digit number.

2: My Tools
	This will take you to a page listing all the tools either belonging to you,
	or currently being borrowed by you.
	If you click on a tool that belongs to you,
	you will have the option to mark it as returned if it has been borrowed, or you
	can edit the information of the tool, if it's not being borrowed.
	Tools as of now simply have a tool_type which specifies what kind of tool it is,
	and is a free field for the user to decide what to do with. We decided to do this
	because at this stage of the testing, when we aren't comfortable with forms, it
	is a little complicated to manage a list of possible tools. They also have a
	description for whatever they wish to add, and an option to mark it as unavailable
	if they choose to.
	If you click the new tool button on the My Tools page, you will be taken to a
	registration page very similar to the tool editing page, where you can create a new
	tool to share.
	If you select a tool you're currently borrowing, you will be taken to that tool's
	page and have the option to return it.

3: Browse Tools
	This will take you to a page listing all of the tools belonging to people in your
	community (for now represented by zipcode), and will not display tools that belong
	to you or are unavailable.
	Clicking a tool in this list will bring you to the tool's page and allow you to
	borrow it. For now, borrowing and sharing is simply done on an honor system and
	not verified by the owner. There is no notification, it simply updates the information
	in the system to mark the tool as unavailable and being held by the borrower.
	If the owner wishes they can mark the tool as returned and the system will revert
	to how it was prior to the borrower making the "request"

4: Log Out
	Self explanatory, should take you back to the main page.