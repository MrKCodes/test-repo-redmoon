# CICD approach

Here we have two approaches:

- Running Ansible playbooks via Jenkins
- Deploying using Jenkins agent

## Approach 1 - Ansible through Jenkins

---

Ideal for current scenario to minimize the overhead and reuse as much as possible

---

Considering ansible has all the steps from cloning, configuring and docker steps.
As soon as there is a new commit on the **develop** branch, the job will be triggered.
What will job do? It will invoke ansible commands from the jenkins server which will be used as Ansible host as well.

This will reuse all the ansible scripts, there needs not be redefine all the automation in any other format.

Lets see an example

```Groovy
node
{
    stage("Installing pre-requiste")
    {
        sh """
            cd /repo/ansible_dir/
            pip3 install poetry
            poetry install
            ansible-galaxy install -r requirements.yml --roles-path ./roles
        """
    }
    stage("Deploy to dev")
    {
        // reusing the pre-existing playbooks
        sh """
            ansible-playbook -i inventories/dev.yml deploy.yml --skip-tags bootstrap
        """
    }
}
```

## Approach 2 - Using Jenkins agent

---

Ideal for generic scenario or a new CICD setup

---

All the dev or staging machines will be set as jenkins agent. So, jenkins can run any code, or copy/delete any file/s on these machines.
Then in the jenkins pipeline job, all the steps need to be defined again without the ansible.

The deployment steps can be defined either in Groovy or shell script with groovy.
Lets take an example of runnin docker command using this approach.

```Groovy
// Running on master-slave architecture
node("test-dev")
{
    stage("Docker run")
    {
        sh """
            docker build -t test-nginx .
            docker run --name test-nginx -d -p 80:80 test-nginx
        """
    }
 }
```

This way all the steps in the stages will be defined. The _test-dev_ is the label expression or alias given to the DEV machine.

## Triggers

---

Lets talk about the triggers.

There are two ways to trigger the Jenkins job.

- SCM polling

  - Jenkins will check the repository for new commits at a particular interval of time, lets say 1 minute.
  - If there is no new commit on the develop branch this will not activate the trigger.
  - If there are any changes in the dev branch, the next polling will detect it the next run, and will activate the trigger.

- BitBucket webhook
  - Need to add a webhook to the repo settings.
  - I will need access to the repo or I can provide the details and you just create it there.
  - As soon as there are changes in the repo this webhook will trigger the jenkins job.
  - If bitbucket server is able to access the jenkins server publicly then this one is the best option.
