<div align="center" >
  <img src="https://github.com/SiddhantTotade/CerGen-Frontend/blob/master/app_images/Paper.png" />
</div>

# About the project

PaperLess is a web application that generates PDF document from HTML templates.
 
### Technologies used

![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue) &nbsp; ![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green) &nbsp; ![Django](https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white) &nbsp; ![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB) &nbsp; ![Typescript](https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white) &nbsp; ![Tanstack Query](https://img.shields.io/badge/TanStack-F6E05E?style=for-the-badge&logo=reactquery&logoColor=black
) &nbsp; ![Shadcn UI](https://img.shields.io/badge/shadcn/ui-000000?style=for-the-badge&logo=shadcnui&logoColor=white
) &nbsp; ![Tailwind Css](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white) &nbsp; ![GraphQL](https://img.shields.io/badge/GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white) &nbsp; ![REST Api](https://img.shields.io/badge/REST_API-005571?style=for-the-badge&logo=api&logoColor=white)

# Getting Started

## Setting Up Virtual Environment

- Clone the project

```shell
git clone git@github.com:SiddhantTotade/PaperLess.git
```

- Open the project in the terminal. The below command opens the project in vs-code but you can choose any editor

```shell
code .
```

- In the terminal type command to create a virtual environment. Prefer root directory for `venv`

  - The below command create a virtual environment in a specific directory

  ```shell
  python -m venv <name_of_venv>
  ```

  <div align="center">
  OR
  </div>
  &nbsp;

  - The below command create a virtual envvironment in the current directory

  ```shell
  python -m venv .
  ```

- After creating `venv`, Activate it. Go to the directory in which the `venv` exists and type command

```shell
source bin/activate
```

- Deactivate the virtual environment.

```shell
deactivate
```

- Before installing the `requirements.txt` check if there is something exists or not. If the command shows nothing then nothing is installed yet

```shell
pip freeze
```

- After activating `venv`, install the `requirements.txt`.

```shell
pip install -r requirements.txt
```

## Setting Up Application

- After enabling the `venv`, run the command for creating migrations

```shell
python manage.py makemigrations
```

- After creating the migrations of all the models, run command

```shell
python manage.py migrate
```

## First - Running Django Server

- Change directory to `paperless`

```shell
cd paperless
```

- Run the django serever

```shell
python manage.py runserver
```

#### Leave a star if you like the project. :star:

### Enjoy :relaxed: :relaxed:

## Project Images

<div align="center" gap="10px" display="flex">

<img src="https://github.com/SiddhantTotade/certificate-generator-and-sender/blob/main/app_images/certificate_before.png" width="400px" />
<img src="https://github.com/SiddhantTotade/certificate-generator-and-sender/blob/main/app_images/certificate_after.png" width="400px" />

<div/>



