%bcond_with bootstrap
%bcond_without junit5
%global git_tag tycho-%{version}
%global fp_p2_git_tag 290f67a4c717599b2f5166ea89aa5365571314b1
%global fp_p2_version 0.0.1
%global fp_p2_snap -SNAPSHOT
%global xmvn_libdir %(realpath $(dirname $(readlink -f $(which xmvn)))/../lib)
%define __requires_exclude osgi*
Name:                tycho
Version:             1.3.0
Release:             6
Summary:             Plugins and extensions for building Eclipse plugins and OSGI bundles with Maven
License:             ASL 2.0 and EPL-1.0
URL:                 http://eclipse.org/tycho
Source0:             http://git.eclipse.org/c/tycho/org.eclipse.tycho.git/snapshot/org.eclipse.tycho-%{git_tag}.tar.xz
Source1:             https://github.com/rgrunber/fedoraproject-p2/archive/%{fp_p2_git_tag}/fedoraproject-p2-%{fp_p2_git_tag}.tar.gz
Source2:             EmptyMojo.java
Source3:             tycho-scripts.sh
Source4:             tycho-bootstrap.sh
Source5:             tycho-debundle.sh
Source6:             p2-install.sh
%if %{with bootstrap}
Source10:            eclipse-bootstrap-photon.tar.xz
%endif
# Submitted upstream: https://bugs.eclipse.org/bugs/show_bug.cgi?id=537963
Patch0:              0001-Bug-537963-Make-the-default-EE-Java-1.8.patch
# Merged upstream: https://git.eclipse.org/c/tycho/org.eclipse.tycho.git/commit/?id=a437fb8870761d733199392f25a8c0e4f34caae9
Patch1:              0002-Bug-543850-Update-artifactcomparator-asm-dep-to-7.0.patch
# Port to latest version of Mockito 2.x
Patch2:              0003-Port-to-latest-versio-of-Mockito.patch
Patch3:              0004-Implement-a-custom-resolver-for-Tycho-in-local-mode.patch
Patch4:              0005-Fix-build-fail.patch
Patch5:              0006-Tycho-should-always-delegate-artifact-resolution-to-.patch
#Patch from: https://git.eclipse.org/c/tycho/org.eclipse.tychogit/commit/?id=43a0e167e39ffaafa5c0e70fbc0ea0b87828f1b3
Patch6:              tweaking-the-products-to-use-httpclient45-feature.patch
# Upstream Eclipse no longer supports non-64bit arches
ExcludeArch:         s390 %{arm} %{ix86}
BuildArch:           noarch
BuildRequires:       maven-local mvn(biz.aQute.bnd:bnd-maven-plugin) mvn(com.beust:jcommander)
BuildRequires:       mvn(de.pdark:decentxml) mvn(junit:junit)
BuildRequires:       mvn(org.apache.commons:commons-compress) mvn(org.apache.commons:commons-exec)
BuildRequires:       mvn(org.apache.commons:commons-lang3) mvn(org.apache.felix:maven-bundle-plugin)
BuildRequires:       mvn(org.apache.maven:maven-archiver) mvn(org.apache.maven:maven-compat)
BuildRequires:       mvn(org.apache.maven:maven-core) mvn(org.apache.maven:maven-plugin-api)
BuildRequires:       mvn(org.apache.maven.plugins:maven-clean-plugin)
BuildRequires:       mvn(org.apache.maven.plugins:maven-dependency-plugin)
BuildRequires:       mvn(org.apache.maven.plugins:maven-install-plugin)
BuildRequires:       mvn(org.apache.maven.plugins:maven-plugin-plugin)
BuildRequires:       mvn(org.apache.maven.plugins:maven-source-plugin)
BuildRequires:       mvn(org.apache.maven.plugin-testing:maven-plugin-testing-harness)
BuildRequires:       mvn(org.apache.maven.plugin-tools:maven-plugin-annotations)
BuildRequires:       mvn(org.apache.maven.shared:maven-verifier)
BuildRequires:       mvn(org.apache.maven.surefire:maven-surefire-common)
BuildRequires:       mvn(org.apache.maven.surefire:surefire-api)
BuildRequires:       mvn(org.codehaus.plexus:plexus-archiver)
BuildRequires:       mvn(org.codehaus.plexus:plexus-compiler-api)
BuildRequires:       mvn(org.codehaus.plexus:plexus-compiler-manager)
BuildRequires:       mvn(org.codehaus.plexus:plexus-component-annotations)
BuildRequires:       mvn(org.codehaus.plexus:plexus-component-metadata)
BuildRequires:       mvn(org.codehaus.plexus:plexus-container-default)
BuildRequires:       mvn(org.codehaus.plexus:plexus-utils) mvn(org.eclipse.jdt:ecj)
BuildRequires:       mvn(org.fedoraproject.xmvn:xmvn-api) mvn(org.fedoraproject.xmvn:xmvn-core)
BuildRequires:       mvn(org.fedoraproject.xmvn:xmvn-install)
BuildRequires:       mvn(org.fedoraproject.xmvn:xmvn-parent:pom:) mvn(org.hamcrest:hamcrest-core)
BuildRequires:       mvn(org.mockito:mockito-core) mvn(org.ow2.asm:asm-tree)
BuildRequires:       mvn(org.ow2.asm:asm-util) mvn(org.slf4j:slf4j-api) mvn(org.slf4j:slf4j-simple)
%if %{with junit5}
BuildRequires:       mvn(org.apache.maven.surefire:surefire-junit-platform)
BuildRequires:       mvn(org.apiguardian:apiguardian-api) mvn(org.opentest4j:opentest4j)
%endif
%if ! %{with bootstrap}
BuildRequires:       %{name} eclipse-platform >= 1:4.11
%else
BuildRequires:       osgi(com.ibm.icu) osgi(org.apache.commons.jxpath) osgi(org.apache.batik.css)
BuildRequires:       osgi(org.kxml2) osgi(org.sat4j.core) osgi(org.sat4j.pb) osgi(org.w3c.css.sac)
BuildRequires:       osgi(javax.servlet-api) osgi(javax.servlet.jsp)
%endif
Requires:            maven-local xmvn-minimal >= 3 ecj >= 1:4.7.3a-1
%if ! %{with bootstrap}
Requires:            eclipse-platform >= 1:4.11
%endif
Requires:            maven-clean-plugin
%description
Tycho is a set of Maven plugins and extensions for building Eclipse
plugins and OSGI bundles with Maven. Eclipse plugins and OSGI bundles
have their own metadata for expressing dependencies, source folder
locations, etc. that are normally found in a Maven POM. Tycho uses
native metadata for Eclipse plugins and OSGi bundles and uses the POM
to configure and drive the build. Tycho supports bundles, fragments,
features, update site projects and RCP applications. Tycho also knows
how to run JUnit test plugins using OSGi runtime and there is also
support for sharing build results using Maven artifact repositories.
Tycho plugins introduce new packaging types and the corresponding
lifecycle bindings that allow Maven to use OSGi and Eclipse metadata
during a Maven build. OSGi rules are used to resolve project
dependencies and package visibility restrictions are honored by the
OSGi-aware JDT-based compiler plugin. Tycho will use OSGi metadata and
OSGi rules to calculate project dependencies dynamically and injects
them into the Maven project model at build time. Tycho supports all
attributes supported by the Eclipse OSGi resolver (Require-Bundle,
Import-Package, Eclipse-GenericRequire, etc). Tycho will use proper
classpath access rules during compilation. Tycho supports all project
types supported by PDE and will use PDE/JDT project metadata where
possible. One important design goal in Tycho is to make sure there is
no duplication of metadata between POM and OSGi metadata.

%package javadoc
Summary:             Javadocs for %{name}
%description javadoc
This package contains the API documentation for %{name}.

%prep
%setup -q -n org.eclipse.tycho-%{git_tag} -a 1
mv fedoraproject-p2-%{fp_p2_git_tag} fedoraproject-p2
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%pom_remove_plugin :maven-site-plugin
%if %{without junit5}
%pom_disable_module org.eclipse.tycho.surefire.junit5 tycho-surefire
%pom_remove_dep ":org.eclipse.tycho.surefire.junit5" tycho-surefire/tycho-surefire-plugin
%endif
find . -name "*.java" | xargs sed -i 's/org.sonatype.aether/org.eclipse.aether/g'
find . -name "*.java" | xargs sed -i 's/org.eclipse.aether.util.DefaultRepositorySystemSession/org.eclipse.aether.DefaultRepositorySystemSession/g'
sed -i 's/public int getPriority/public float getPriority/g' tycho-core/src/main/java/org/eclipse/tycho/core/p2/P2RepositoryConnectorFactory.java
mkdir -p tycho-maven-plugin/src/main/java/org/fedoraproject
pushd tycho-maven-plugin/src/main/java/org/fedoraproject
cp %{SOURCE2} .
popd
sed -i '/^<unit id=.*$/d' tycho-bundles/tycho-bundles-target/tycho-bundles-target.target
%pom_xpath_remove "pom:dependency[pom:classifier='sources' and pom:artifactId='commons-compress']" tycho-p2/tycho-p2-director-plugin
for mod in tycho-bundles/org.eclipse.tycho.{p2.{maven.repository.tests,resolver.impl.test,tools.tests},test.utils,core.shared.tests}; do
  sed -i 's/^Require-Bundle://
          /org\.junit/ i Require-Bundle: org.hamcrest.core,' \
          $mod/META-INF/MANIFEST.MF
done
sed -i -e '/tycho-testing-harness/a<version>${project.version}</version>' tycho-surefire/tycho-surefire-plugin/pom.xml
%if %{with bootstrap}
%pom_xpath_remove "pom:compilerId" tycho-lib-detector
%pom_remove_dep "org.eclipse.tycho:tycho-compiler-jdt" tycho-lib-detector
for b in core.shared.tests p2.resolver.impl.test p2.resolver.shared.tests p2.maven.repository.tests p2.tools.tests test.utils ; do
  %pom_disable_module org.eclipse.tycho.$b tycho-bundles
done
%pom_disable_module org.fedoraproject.p2.tests fedoraproject-p2
%pom_remove_dep -r :::test
tar -xf %{SOURCE10}
pushd bootstrap
for f in usr/lib/eclipse/plugins/org.eclipse.osgi.compatibility.state_*.jar \
         usr/lib/eclipse/plugins/org.eclipse.osgi_*.jar ; do
  xmvn -o install:install-file -Dfile=$f -Dpackaging=jar -DgroupId=org.eclipse.tycho -Dmaven.repo.local=$(pwd)/../.m2 \
    -DartifactId=$(echo $(basename $f) | cut -d_ -f1) -Dversion=$(echo "${f%.jar}" | cut -d_ -f2)
done
popd
cp %{SOURCE3} %{SOURCE4} .
chmod 777 tycho-bootstrap.sh
./tycho-bootstrap.sh %{version}
%else
sysVer=`grep -C 1 "<artifactId>tycho</artifactId>" %{_mavenpomdir}/tycho/tycho.pom | grep "version" | sed 's/.*>\(.*\)<.*/\1/'`
mkdir boot
sed -e 's/ns[0-9]://g' %{_datadir}/maven-metadata/tycho.xml > boot/tycho-metadata.xml
for pom in $(grep 'pom</path>' boot/tycho-metadata.xml | sed 's|.*>\(.*\)<.*|\1|'); do
    sed -e "s/>$sysVer/>%{version}-SNAPSHOT/g" -e "s/%{fp_p2_version}%{fp_p2_snap}/%{fp_p2_version}/" <$pom >boot/$(basename $pom)
done
cp -p $(build-classpath tycho/tycho-maven-plugin) boot/tycho-maven-plugin.jar
jar xf boot/tycho-maven-plugin.jar META-INF/plexus/components.xml
sed -i s/$sysVer/%{version}-SNAPSHOT/ META-INF/plexus/components.xml
jar uf boot/tycho-maven-plugin.jar META-INF/plexus/components.xml
sed -i '
  s|>/[^<]*/\([^/]*\.pom\)</path>|>'$PWD'/boot/\1</path>|
  s|>'$sysVer'</version>|>%{version}-SNAPSHOT</version><compatVersions><version>%{version}-SNAPSHOT</version></compatVersions>|
  s|>'%{fp_p2_version}%{fp_p2_snap}'</version>|>%{fp_p2_version}</version><compatVersions><version>%{fp_p2_version}</version></compatVersions>|
  s|%{_javadir}/tycho/tycho-maven-plugin.jar|'$PWD'/boot/tycho-maven-plugin.jar|
' boot/tycho-metadata.xml
%mvn_config resolverSettings/metadataRepositories/repository $PWD/boot/tycho-metadata.xml
%endif
%pom_add_plugin :maven-clean-plugin tycho-bundles/tycho-standalone-p2-director "
<executions>
  <execution>
    <id>default-clean-1</id>
    <phase>initialize</phase>
    <configuration>
      <skip>true</skip>
    </configuration>
  </execution>
</executions>"
%pom_xpath_inject "pom:modules" "<module>fedoraproject-p2</module>"

%build
%mvn_build -f -- \
  -Dtycho-version=%{version}-SNAPSHOT -DtychoBootstrapVersion=%{version}-SNAPSHOT \
  -Dmaven.repo.local=$(pwd)/.m2 -Dfedora.p2.repos=$(pwd)/bootstrap
%mvn_artifact fedoraproject-p2/org.fedoraproject.p2/pom.xml
sed -i -e 's|type>eclipse.*<|type>jar<|' .xmvn-reactor
%mvn_package "::target::" __noinstall
%mvn_package ":org.fedoraproject.p2.tests" __noinstall

%install
cp %{SOURCE3} %{SOURCE5} .
%if ! %{with bootstrap}
chmod 777 tycho-debundle.sh
./tycho-debundle.sh $(pwd)/tycho-bundles/tycho-bundles-external \
  $(pwd)/tycho-bundles/tycho-bundles-external/target/tycho-bundles-external-manifest.txt
./tycho-debundle.sh $(pwd)/tycho-bundles/tycho-standalone-p2-director
%endif
%if %{with bootstrap}
for b in org.eclipse.osgi \
         org.eclipse.osgi.compatibility.state ; do
  osgiJarPath=$(find .m2/org/eclipse/tycho/$b/*/ -name "*.jar")
  osgiPomPath=$(find .m2/org/eclipse/tycho/$b/*/ -name "*.pom")
  %mvn_artifact $osgiPomPath $osgiJarPath
  %mvn_alias "org.eclipse.tycho:$b" "org.eclipse.osgi:$b"
done
%endif
%mvn_install
%if ! %{with bootstrap}
install -pm 644 tycho-bundles/tycho-bundles-external/target/tycho-bundles-external-manifest.txt %{buildroot}%{_javadir}/tycho
%add_maven_depmap org.eclipse.tycho:tycho-bundles-external:txt:manifest:%{version} tycho/tycho-bundles-external-manifest.txt
%endif
%if %{with bootstrap}
for bnd in \
  core.contenttype \
  core.expressions \
  core.filesystem \
  core.jobs \
  core.net \
  core.resources \
  core.runtime \
  equinox.app \
  equinox.common \
  equinox.concurrent \
  equinox.preferences \
  equinox.registry \
  equinox.security ; do
bndJarPath=$(find bootstrap -name "org.eclipse.${bnd}_*.jar")
install -m 644 -T $bndJarPath $RPM_BUILD_ROOT%{_javadir}/tycho/$bnd.jar
done
%endif
sed -i '/<resolvedVersion>/d' %{buildroot}%{_datadir}/maven-metadata/tycho.xml
install -dm 755 %{buildroot}%{_javadir}-utils/
install -pm 755 %{SOURCE6} %{buildroot}%{_javadir}-utils/
install -dm 755 %{buildroot}%{xmvn_libdir}/installer/
%if %{with bootstrap}
ln -s %{_javadir}/tycho/org.eclipse.osgi.jar %{buildroot}%{xmvn_libdir}/installer/
%else
ln -s %{_javadir}/eclipse/osgi.jar %{buildroot}%{xmvn_libdir}/installer/
%endif
ln -s %{_javadir}/tycho/xmvn-p2-installer-plugin.jar %{buildroot}%{xmvn_libdir}/installer/
ln -s %{_javadir}/tycho/org.fedoraproject.p2.jar %{buildroot}%{xmvn_libdir}/installer/

%files -f .mfiles
%{xmvn_libdir}/installer/*
%{_javadir}-utils/p2-install.sh
%if %{with bootstrap}
%{_javadir}/tycho/core.*.jar
%{_javadir}/tycho/equinox.*.jar
%endif
%doc README.md

%files javadoc -f .mfiles-javadoc

%changelog
* Wed Jul 13 2022 xiaoqianlv <xiaoqian@nj.iscas.ac.cn> - 1.3.0-6
- non-bootstrap build for riscv

* Wed Jul 13 2022 xiaoqianlv <xiaoqian@nj.iscas.ac.cn> - 1.3.0-5
- bootstrap build for riscv

* Fri May 06 2022 chenchen <chen_aka_jan@163.com> - 1.3.0-4
- tweaking the products to use httpclient45 feature

* Sun Sep 13 2020 yanan li <liyanan032@huawei.com> - 1.3.0-3
- fix build fail

* Sat Sep 05 2020 maminjie <maminjie1@huawei.com> - 1.3.0-2
- support local mode

* Fri Aug 21 2020 maminjie <maminjie1@huawei.com> - 1.3.0-1
- package init
