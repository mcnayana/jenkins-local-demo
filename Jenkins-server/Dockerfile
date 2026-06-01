FROM jenkins/jenkins:lts-jdk17

USER root

# Install required tools
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    docker.io \
    && rm -rf /var/lib/apt/lists/*

# Skip Jenkins setup wizard
ENV JAVA_OPTS="-Djenkins.install.runSetupWizard=false"

# Install Jenkins plugins
COPY plugins.txt /usr/share/jenkins/ref/plugins.txt

RUN jenkins-plugin-cli --plugin-file /usr/share/jenkins/ref/plugins.txt

# Give Jenkins access to Docker
RUN groupadd -f docker && \
    usermod -aG docker jenkins

# Switch back to Jenkins user
USER jenkins

EXPOSE 8080 50000

VOLUME /var/jenkins_home