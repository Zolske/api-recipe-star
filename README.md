# Recipe Star API
This is the backend application for the frontend application "Recipe Star".  
**link to the frontend application ->** ["Recipe Star"](https://recipe-star.herokuapp.com/)  
**link to the backend application ->** ["Recipe Star API"](https://recipe-star-api.herokuapp.com/)  
**link to the frontend GitHub repository ->** ["recipe-star"](https://github.com/Zolske/recipe-star/blob/main/README.md)
***
## Setup and Deployment  
*Please, click the link below to get to the "Setup and Deployment" document.*  
**link to ->** [setup and deployment](./assets/doc/setup_deployment_api.md)  
***
  ## API endpoints

  | Methods                  | PROFILES <br> _name, content_ | RECIPE <br> _images, title, category, filter_category, ingredients, instruction_ | COMMENTS <br> _content_ | LIKES <br> _id_ | FOLLOWERS <br> _id_ |
  | ------------------------ | :---------------------------: | :------------------------------------------------------------------------------: | :---------------------: | :-------------: | :-----------------: |
  | **create /<br> RECIPES** |              no               |                                       yes                                        |           yes           |       yes       |         yes         |
  | **retrieve<br> GET**     |              yes              |                                       yes                                        |           yes           |       yes       |         yes         |
  | **update<br> PUT**       |              yes              |                                       yes                                        |           yes           |       no        |         no          |
  | **destroy<br>DELETE**    |              no               |                                       yes                                        |           yes           |       yes       |         yes         |
  | **list<br>GET**          |              yes              |                                       yes                                        |           yes           |       yes       |         yes         |
  | **search<br>GET**        |              no               |                                       yes                                        |           no            |       no        |         no          |

  | Authentication |  registration <br> **POST**   |      login <br> **POST**       |       logout <br> **POST**       |
  | -------------- | :---------------------------: | :----------------------------: | :------------------------------: |
  | endpoint       | "/dj-rest-auth/registration/" |     "/dj-rest-auth/login/"     |     "/dj-rest-auth/logout/"      |
  | expected value | username password1 password2  |       username password        |
  |                |       **user <br> GET**       |  **refresh token <br> POST**   |  **change password <br> POST**   |
  | endpoint       |    "/dj-rest-auth/logout/"    | "/dj-rest-auth/token/refresh/" | "/dj-rest-auth/password/change/" |
  | expected value |                               |         refresh token          |   new_password1 new_password2    |
***
## Disclaimer  
The rest of the documentation is merged with the documentation of the frontend application "Recipe Star".  
**link to the frontend GitHub repository ->** ["recipe-star"](https://github.com/Zolske/recipe-star/blob/main/README.md)  
   
The code is based on  "Adam Lapinski's" walk-through project "Moments"!
https://github.com/Code-Institute-Solutions/moments

