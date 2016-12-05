image::https://badges.gitter.im/Join%20Chat.svg[Gitter,link=https://gitter.im/spring-projects/spring-security?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge]

image:https://travis-ci.org/spring-projects/spring-security.svg?branch=master["Build Status", link="https://travis-ci.org/spring-security/spring-security"]

= Spring Security

Spring Security provides security services for the http://docs.spring.io[Spring IO Platform]. Spring Security 3.1 requires Spring 3.0.3 as
a minimum and also requires Java 5.

For a detailed list of features and access to the latest release, please visit http://spring.io/projects[Spring projects].

== Code of Conduct
This project adheres to the Contributor Covenant link:CODE_OF_CONDUCT.adoc[code of conduct].
By participating, you  are expected to uphold this code. Please report unacceptable behavior to spring-code-of-conduct@pivotal.io.

== Downloading Artifacts
See https://github.com/spring-projects/spring-framework/wiki/Downloading-Spring-artifacts[downloading Spring artifacts] for Maven repository information.

== Documentation
Be sure to read the http://docs.spring.io/spring-security/site/docs/current/reference/htmlsingle/[Spring Security Reference].
Extensive JavaDoc for the Spring Security code is also available in the http://docs.spring.io/spring-security/site/docs/current/apidocs/[Spring Security API Documentation].

== Quick Start
We recommend you visit http://docs.spring.io/spring-security/site/docs/current/reference/htmlsingle/[Spring Security Reference] and read the "Getting Started" page.

== Building from Source
Spring Security uses a http://gradle.org[Gradle]-based build system.
In the instructions below, http://vimeo.com/34436402[`./gradlew`] is invoked from the root of the source tree and serves as
a cross-platform, self-contained bootstrap mechanism for the build.

=== Prerequisites
http://help.github.com/set-up-git-redirect[Git] and the http://www.oracle.com/technetwork/java/javase/downloads[JDK7 build].

Be sure that your `JAVA_HOME` environment variable points to the `jdk1.7.0` folder extracted from the JDK download.

=== Check out sources
[indent=0]
----
git clone git@github.com:spring-projects/spring-security.git
----

=== Install all spring-\* jars into your local Maven cache
[indent=0]
----
./gradlew install
----

=== Compile and test; build all jars, distribution zips, and docs
[indent=0]
----
./gradlew build
----

Discover more commands with `./gradlew tasks`.
See also the https://github.com/spring-projects/spring-framework/wiki/Gradle-build-and-release-FAQ[Gradle build and release FAQ].

== Getting Support
Check out the http://stackoverflow.com/questions/tagged/spring-security[Spring Security tags on Stack Overflow].
http://spring.io/services[Commercial support] is available too.

== Contributing
http://help.github.com/send-pull-requests[Pull requests] are welcome; see the https://github.com/spring-projects/spring-security/blob/master/CONTRIBUTING.md[contributor guidelines] for details.

== License
Spring Security is Open Source software released under the
http://www.apache.org/licenses/LICENSE-2.0.html[Apache 2.0 license].
