const { python, SampleFile, SampleReadme, Component, projectType } = require("projen");
const { PythonProject } = require("projen/lib/python");
const fs  = require("fs")
const path = require("path")


replacements = [
  { 
    key: '<<name>>',
    replacement: process.env.NAME
  },
  {
    key: '<<cdkqualifier>>',
    replacement: process.env.CDKQUALIFIER
  },
  {
    key: '<<account>>',
    replacement: process.env.ACCOUNT
  },
  {
    key: '<<region>>',
    replacement: process.env.REGION
  },
  {
    key: '<<repo>>',
    replacement: process.env.REPONAME
  },
  {
    key: '<<githubtoken>>',
    replacement: process.env.GITHUBTOKEN
  }
]

const venv = ['.',process.env.NAME].join('');
const desc = 'a cdk2 project';

const getprojectfiles = function(dirPath, arrayOfFiles) {
  files = fs.readdirSync(dirPath)

  arrayOfFiles = arrayOfFiles || []

  files.forEach(function(file) {
    if (fs.statSync(dirPath + "/" + file).isDirectory()) {
      arrayOfFiles = getprojectfiles(dirPath + "/" + file, arrayOfFiles)
    } else {
      arrayOfFiles.push(path.join(__dirname, dirPath, "/", file))
    }
  })
  return arrayOfFiles
}


const project = new python.PythonProject({
  name: process.env.NAME,
  moduleName: process.env.NAME,               
  version: "2.0.0",
  description: desc,  /* A short description of the package. */
  outdir: 'projen.out',
  deps: [
    'Pydantic',
    'boto3',
    'aws-cdk-lib',
		'constructs',
    'PyYaml',
    //'atamai-cdk.atamai-pipeline'
  ],                /* List of runtime dependencies for this project. */
  // devDeps: [],             /* List of dev dependencies for this project. */
  pip: true,               /* Use pip with a requirements.txt file to track project dependencies. */
  pytest: true,            /* Include pytest tests. */
  setuptools: false,   /* Use setuptools with a setup.py script for packaging and publishing. */
  venv: true,              /* Use venv to manage a virtual environment for installing dependencies inside. */
  venvOptions: { envdir: venv},
  sample: false,     /* dont' create any sample code.  */
  readme: {contents: ('Cdk2 Project for ' + process.env.NAME)},   /*TODO this could be expanded otu with some instructions */
  github: false,
});


project.gitignore.addPatterns(venv);    // note this can be a list of thigns to ignore, but i'm just adding the newly created venv
project.gitignore.addPatterns('.projen');


templates = getprojectfiles('templates');


templates.forEach((path, index, array) => {
    projectpath = path.split("templates/")[1];
    console.log('\n',projectpath);
    let template = fs.readFileSync(path).toString('utf-8');

    replacements.forEach((key, index, array) => {
      template = template.replace(key.key, key.replacement);
    })

    console.log(template);
    new SampleFile(project, projectpath,
       {
         contents: template
    });
})


project.synth();
