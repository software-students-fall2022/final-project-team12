![Building & Testing](https://github.com/software-students-fall2022/final-project-team12/actions/workflows/build.yaml/badge.svg)
![Continuous Deployment](https://github.com/software-students-fall2022/final-project-team12/actions/workflows/deploy.yaml/badge.svg)

[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-c66648af7eb3fe8bc4f294546bfd86ef473780cde1dea487d3c4ff354943c9ae.svg)](https://classroom.github.com/online_ide?assignment_repo_id=9572803&assignment_repo_type=AssignmentRepo)

# Final Project


## Project Description
**Cook Book** - A recipe collection web app for everyone interested/involved in cooking, where users can add/edit their recipes and share them with other users. User can also save and unsave recipes in their accounts and add comments to other recipes to share their feedback.

**Database** 
- Stores each user's username and password, as well as their recipes.
- Stores each recipe, the details of the recipe and the comments on the recipe.

## Running the Project Locally (using Docker Compose)
- Make sure Docker Desktop is installed, if not,

    check [here](https://docs.docker.com/desktop/install/windows-install/) for windows

    check
    [here](https://docs.docker.com/desktop/install/mac-install/) for mac

- Clone this repository to your local machine
- Once the docker desktop is installed, make sure you go to the top right corner and click on bug sign to navigate to **RESET TO FACTORY DEFAULTS**. This will reset Docker and prompt Docker to restart. Please make sure you do this step before running the files from github repository because the docker does not create right images sometimes (you won't always have to do this, but do it just in case).
- Go to the root folder (final-project-team12) and run the following command
    ```
    docker-compose up
    ```
- This will install all the required dependencies and the web app starts running at port **127.0.0.1:3000**. Make sure you go to **127.0.0.1:3000** port because the docker outputs the web-app at **127.0.0.1:3000** port.

## Deployed App on Digital Ocean
Find our deployed web app here: [Cook Book](https://cookbook-zkup6.ondigitalocean.app/).

## Docker Hub Image
Find our Docker Hub image for the project [here](https://hub.docker.com/repository/docker/ma5938/cookbook). 

## Team Members

[Dixit Timilsina](https://github.com/dt1930)

[Maaz Ahmed](https://github.com/maazahmedd)

[Sanjaya Bhatta](https://github.com/itSanjaya)

[Fatema Nassar](https://github.com/fnassar)

[Elyazya Al Kobaisi](https://github.com/elyazya)

