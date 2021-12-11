const { python, SampleFile, SampleReadme, Component, projectType } = require("projen");
const { PythonProject } = require("projen/lib/python");
const fs  = require("fs")
const path = require("path")

var name = process.env.NAME;
var account = process.env.ACCOUNT;
var region = process.env.REGION
var locallookupprofile = process.env.LOCALLOOKUPPROFILE; // # this is a local profile to use if you are running locally. should be pointing to candi account
var lookuprole = process.env.LOOKUPROLE;

replacements = [
  { 
    key: '<<name>>',
    replacement: name
  },
  { 
    key: '<<account>>',
    replacement: account
  },
  { 
    key: '<<region>>',
    replacement: region
  },
  { 
    key: '<<locallookupprofile>>',
    replacement: locallookupprofile
  },
  { 
    key: '<<lookuprole>>',
    replacement: lookuprole
  },
]



const venv = ['.',name].join('');
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
  name: name,
  moduleName: name,               
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
  readme: {contents: ('Cdk2 Project for ' + name)},   /*TODO this could be expanded otu with some instructions */
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
