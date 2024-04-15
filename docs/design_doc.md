# Team B1 Design Document

## Title and Team
- XL News Feed and Announcement System 
- Embrey Morton, Jayson Mbugua, Alphonzo Dixon, Ishmael Percy


## Overview
The CSXL and student organizations need the ability to post and update news on the CSXL website to share necessary announcements. The news feed would be available to all students with access to the CSXL website. When it comes to posting announcements only the root has access to do so, if a student organization wants to do so they can create a post request where they can create the post. After going through several steps of approval it can finally be uploaded for all to see.
 

## Key Personas

1. Sally Student can view all news updates from both the CSXL and student organizations from the newly routed home page. Sally Student can also propose post ideas that ultimately an administrator must approve and post to the feed.

2. Amy Ambassador can review incoming post requests to speed up the process of a post getting approved. Amy Ambassador can essentially work as the “middleman” to ensure that all post details are accurate.

3. Rhonda Root can approve/deny incoming posts, edit and create posts at their discretion, as well as delete posts. Rhonda Root has access to the full history with an administrator-only view.

## Wireframes
### Sally Student
![Screenshot 2024-03-25 at 10 11 56 PM](https://github.com/comp423-24s/csxl-final-team-b1/assets/111366508/e79b4a7e-6ae6-4076-8ee8-fe963649baf4)

Sally Student has access to the entire XL news feed, which is the home page of the CSXL website, when loading the CSXL page signed out or logged in it will first display the XL announcements/news feed. To return to the XL news feed from any other sidebar tab, all one has to do is click on the XL logo. By scrolling down one can see all of the posts that have been uploaded for the following week, and if they want to go back further to a previous week they can click between two arrows located at the top of the page. 

![Screenshot 2024-03-25 at 10 12 34 PM](https://github.com/comp423-24s/csxl-final-team-b1/assets/111366508/1c313787-a56f-433f-aaca-2d5c1beaeaab)

When Sally Student clicks on an XL post, she will be redirected to a new view that is created just for announcements, this page will contain all of the information about a post and will be integrated with an arrow on the left and right of the post to allow Sally to click between post one by one. 

### Amy Ambassador
![Screenshot 2024-03-25 at 10 13 38 PM](https://github.com/comp423-24s/csxl-final-team-b1/assets/111366508/73e3b618-4c50-40a8-b321-924901788f66)

After a post form has been filled out it is reviewed by an ambassador, and can then be sent to the root where it must be finally approved. If a post needs some improvements it can be edited by an ambassador. The feature to edit or delete may have to be changed to a system where for a post to be rejected it must go through multiple ambassadors. Also, the process of editing may be changed as well and replaced with a system of sending the post back to the creator with comments about what changes need to be made, this way edits are not that is against what the creator of the post was trying to say.

### Rhonda Root
![Screenshot 2024-03-25 at 10 14 31 PM](https://github.com/comp423-24s/csxl-final-team-b1/assets/111366508/ad80e50d-63b3-4a45-acb9-bda9a03935c0)

Ronda has access to approve or deny a post after it has been approved by the ambassadors, some more features may eventually be added here to allow the root to have more control over all in the pending approval process. 

## Technical Implementation Opportunities and Planning

### Dependencies
- Users: When a post is made, we will need to keep track of the author by connecting it to a user object.

- Organizations: When a post is made, we will need to keep track of the optional organization that the announcement is associated with by connecting it to an organization object.

- Event: When a post is made, we will need to keep track of the optional event that the announcement references by connecting it to an event object.

- Permissions: We will need to leverage the current permission model to keep track of who can create post requests, review posts, and approve/deny posts.

### Extensions
- New database tables and schemas that store information about an announcement
  - Tables will need to have relationships (potentially one-to-many) with the user, organization, and event tables.
  - Will need separate databases to store posts that have been approved and are on the feed as well as one to store drafts and posts that need to be reviewed.

### Page Components and Widgets
- News Feed Component: Create a new tab in the navigation component (also the new home page) that routes to a display of announcements from the current week.

- Individual Post Widget: Create a widget that will be used for displaying posts on the news feed. This widget will display a minimalistic version of the post (Title, short description, date/time, author).

- Individual Post View Component: Create a component that will display the entirety of a post (all 10+ fields) as its own page. Will be routable from the corresponding widget on the news feed. Can also be used to view a draft of a post as “users would see them.”

- Create/Edit Post (Form) Component: A form (potentially) used for inserting and modifying all of the required fields for a post. Can be saved as a draft by the author for later modifications. 

- XL Ambassador Review Post Component: A component that displays the contents of an incoming post request and allows the ambassador to give their “stamp of approval” before it reaches the admin. Potentially can give them the ability to deny and leave suggestions.

- User Admin View/Edit Component: A component that provides a user admin with a similar view to the news feed, however it includes buttons for corresponding CRUD operations.

### Models
- Post: Model used to store all of the information necessary for a post. Encapsulates the:
  1. ID (primary key)
  2. Headline
  3. Synopsis
  4. Main Story (written in Markdown)
  5. Author (relationship to a user)
  6. Organization (optional relationship to an Organization)
  7. State (Draft, Published, Archived)
  8. Slug (unique string used in URL rather than news ID)
  9. Image URL (optional link to an image for use in feed listing)
  10. Publish Date
  11. Modification Date

- Historical Posts: Model used to store all of the posts ever made, which will encapsulate the Post model.

- Eligible Posters (potential): Model used to store users who have been authorized to create and submit post requests.

### API / Routes
- Change the “home” route of the CSXL to the News Feed component.

- GET Posts: Returns the most recent posts in the system (number specified later). 

- GET Posts (by Organization): Returns a list of post models that are associated with the provided organization.

- GET Post (by ID): Returns the post model with the corresponding unique ID.

- POST Post: Receives post information. Used by Rhonda Root after a post has been approved.

- DELETE Post: Deletes a post from the system. Used by Rhonda Root. 

### Security and Privacy Concerns
- Rhonda Root should be the only one who can approve a post that has been reviewed and approved by one or multiple XL ambassadors.

- Amy Ambassador should be able to review posts that come in.

- Rhonda Root is the only one who can delete a post.
