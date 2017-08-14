%ifarch s390 s390x
%global build_openmpi 0
%endif
%{!?build_openmpi:%global build_openmpi 1}
%{!?build_mpich:%global build_mpich 1}
%global pv_maj 5
%global pv_min 4
%global pv_patch 0
%global pv_majmin %{pv_maj}.%{pv_min}
#global rcver RC3

# VTK currently is carrying local modifications to gl2ps
%bcond_with gl2ps
%if !%{with gl2ps}
%global vtk_use_system_gl2ps -DVTK_USE_SYSTEM_GL2PS:BOOL=OFF
%endif

# We need jsoncpp >= 0.7
%if ( 0%{?fedora} && 0%{?fedora} >= 25 ) || 0%{?rhel} >= 8
%global system_jsoncpp 1
%global vtk_use_system_jsoncpp -DVTK_USE_SYSTEM_JSONCPP:BOOL=ON
%else
%global system_jsoncpp 0
%global vtk_use_system_jsoncpp -DVTK_USE_SYSTEM_JSONCPP:BOOL=OFF
%endif

%bcond_without protobuf
%if %{with protobuf}
%global vtk_use_system_protobuf -DVTK_USE_SYSTEM_PROTOBUF:BOOL=ON
%else
%global vtk_use_system_protobuf -DVTK_USE_SYSTEM_PROTOBUF:BOOL=OFF
%endif

# We need pugixml >= 1.4
%if 0%{?fedora} || 0%{?rhel} >= 8
%global system_pugixml 1
%global vtk_use_system_pugixml -DVTK_USE_SYSTEM_PUGIXML:BOOL=ON
%else
%global system_pugixml 0
%global vtk_use_system_pugixml -DVTK_USE_SYSTEM_PUGIXML:BOOL=OFF
%endif

Name:           paraview-legacy
Version:        %{pv_majmin}.%{pv_patch}
Release:        1%{?rcver:.%rcver}%{?dist}
Summary:        Parallel visualization application (legacy OpenGL backend)

License:        BSD
URL:            http://www.paraview.org/
Source0:        http://www.paraview.org/files/v%{pv_majmin}/ParaView-v%{version}%{?rcver:-%rcver}.tar.gz
Source1:        paraview.xml

%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  cmake3
BuildRequires:  qt-assistant
%else
BuildRequires:  cmake
BuildRequires:  qt-assistant-adp-devel
%endif
BuildRequires:  lz4-devel
BuildRequires:  qt-devel
BuildRequires:  qt-webkit-devel
BuildRequires:  mesa-libOSMesa-devel
BuildRequires:  python-devel, tk-devel, hdf5-devel
BuildRequires:  cgnslib-devel
# Fails looking for PythonQt_QtBindings.h
# https://gitlab.kitware.com/paraview/paraview/issues/17365
#BuildRequires:  pythonqt-devel
BuildRequires:  freetype-devel, libtiff-devel, zlib-devel
BuildRequires:  expat-devel
BuildRequires:  readline-devel
BuildRequires:  openssl-devel
BuildRequires:  gnuplot
BuildRequires:  wget
BuildRequires:  boost-devel
BuildRequires:  eigen3-devel
%if 0%{with gl2ps}
BuildRequires:  gl2ps-devel >= 1.3.8
%endif
BuildRequires:  hwloc-devel
%if %{system_jsoncpp}
BuildRequires:  jsoncpp-devel >= 0.7.0
%endif
# Requires patched libharu https://github.com/libharu/libharu/pull/157
#BuildRequires:  libharu-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libpng-devel
BuildRequires:  libtheora-devel
BuildRequires:  libxml2-devel
BuildRequires:  netcdf-cxx-devel
%if %{with protobuf}
BuildRequires:  protobuf-devel
%endif
%if %{system_pugixml}
BuildRequires:  pugixml-devel >= 1.4
%endif
# For validating desktop and appdata files
BuildRequires:  desktop-file-utils
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  libappstream-glib
%endif

Requires:       hdf5 = %{_hdf5_version}
Requires:       %{name}-data = %{version}-%{release}
Requires:       python-pygments
Requires:       python-six
Requires:       python-pygments
Requires:       python-six
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires:       numpy
Requires:       python-twisted-core
%else
Requires:       python2-autobahn
Requires:       python2-numpy
Requires:       python2-twisted
%endif

Obsoletes:      paraview-demos < 3.2.1-4

Provides:       paraview-demos = %{version}-%{release}

# Bundled KWSys
# https://fedorahosted.org/fpc/ticket/555
# Components used are specified in VTK/Utilities/KWSys/CMakeLists.txt
Provides: bundled(kwsys-base64)
Provides: bundled(kwsys-commandlinearguments)
Provides: bundled(kwsys-directory)
Provides: bundled(kwsys-dynamicloader)
Provides: bundled(kwsys-encoding)
Provides: bundled(kwsys-fstream)
Provides: bundled(kwsys-fundamentaltype)
Provides: bundled(kwsys-glob)
Provides: bundled(kwsys-md5)
Provides: bundled(kwsys-process)
Provides: bundled(kwsys-regularexpression)
Provides: bundled(kwsys-system)
Provides: bundled(kwsys-systeminformation)
Provides: bundled(kwsys-systemtools)
# Bundled jsoncpp
%if !0%{system_jsoncpp}
Provides: bundled(jsoncpp) = 0.7.0
%endif
# Bundled protobuf
%if !%{with protobuf}
Provides: bundled(protobuf) = 2.3.0
%endif
# Bundled vtk
# https://bugzilla.redhat.com/show_bug.cgi?id=697842
Provides: bundled(vtk) = 6.3.0
Provides: bundled(diy2)
Provides: bundled(icet)
Provides: bundled(libharu)
Provides: bundled(libproj4)
Provides: bundled(qttesting)
Provides: bundled(xdmf2)

# Do not provide anything in paraview's library directory
%global __provides_exclude_from ^(%{_libdir}/paraview/|%{_libdir}/.*/lib/paraview/).*$
# Do not require anything provided in paraview's library directory
# This list needs to be maintained by hand
%global __requires_exclude ^lib(IceT|QtTesting|vtk%{!?_with_protobuf:|protobuf}).*$


#-- Plugin: VRPlugin - Virtual Reality Devices and Interactor styles : Disabled - Requires VRPN
#-- Plugin: MantaView - Manta Ray-Cast View : Disabled - Requires Manta
#-- Plugin: ForceTime - Override time requests : Disabled - Build is failing
#-- Plugin: VaporPlugin - Plugin to read NCAR VDR files : Disabled - Requires vapor

# We want to build with a system vtk someday, but it doesn't work yet
# -DUSE_EXTERNAL_VTK:BOOL=ON \\\
# -DVTK_DIR=%{_libdir}/vtk \\\

%global paraview_cmake_options \\\
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \\\
        -DTCL_LIBRARY:PATH=tcl \\\
        -DPARAVIEW_BUILD_PLUGIN_AdiosReader:BOOL=ON \\\
        -DPARAVIEW_BUILD_PLUGIN_EyeDomeLighting:BOOL=ON \\\
        -DPARAVIEW_ENABLE_PYTHON:BOOL=ON \\\
        -DPARAVIEW_QT_VERSION:STRING="4" \\\
        -DPARAVIEW_WWW_DIR=%{buildroot}%{_pkgdocdir} \\\
        -DPYTHONQT_DIR=/usr \\\
        -DVTK_CUSTOM_LIBRARY_SUFFIX="" \\\
        -DVTK_INSTALL_DATA_DIR=share/paraview \\\
        -DVTK_INSTALL_PACKAGE_DIR=share/cmake/paraview \\\
        -DVTK_PYTHON_SETUP_ARGS="--prefix=/usr --root=%{buildroot}" \\\
        -DVTK_RENDERING_BACKEND:STRING=OpenGL \\\
        -DVTK_USE_OGGTHEORA_ENCODER:BOOL=ON \\\
        -DVTK_USE_SYSTEM_LIBRARIES=ON \\\
%if 0%{?rhel} && 0%{?rhel} <= 7 \
        -DVTK_USE_SYSTEM_AUTOBAHN:BOOL=OFF \\\
%else \
        -DVTK_USE_SYSTEM_AUTOBAHN:BOOL=ON \\\
%endif \
        -DVTK_USE_SYSTEM_HDF5=ON \\\
        -DVTK_USE_SYSTEM_LIBHARU=OFF \\\
        %{?vtk_use_system_gl2ps} \\\
        %{?vtk_use_system_jsoncpp} \\\
        -DVTK_USE_SYSTEM_NETCDF=ON \\\
        %{?vtk_use_system_protobuf} \\\
        %{?vtk_use_system_pugixml} \\\
        -DVTK_USE_SYSTEM_PYGMENTS:BOOL=ON \\\
        -DVTK_USE_SYSTEM_QTTESTING=OFF \\\
        -DVTK_USE_SYSTEM_TWISTED:BOOL=ON \\\
        -DVTK_USE_SYSTEM_XDMF2=OFF \\\
        -DVTK_USE_SYSTEM_ZOPE:BOOL=ON \\\
        -DXDMF_WRAP_PYTHON:BOOL=ON \\\
        -DBUILD_EXAMPLES:BOOL=ON \\\
        -DBUILD_TESTING:BOOL=OFF \\\
        -DCMAKE_VERBOSE_MAKEFILE:BOOL=ON

%global paraview_cmake_mpi_options \\\
        -DCMAKE_PREFIX_PATH:PATH=$MPI_HOME \\\
        -DCMAKE_INSTALL_PREFIX:PATH=$MPI_HOME \\\
        -DHDF5_INCLUDE_DIRS:PATH=$MPI_INCLUDE \\\
        -DVTK_INSTALL_INCLUDE_DIR:PATH=include/paraview \\\
        -DVTK_INSTALL_ARCHIVE_DIR:PATH=lib/paraview \\\
        -DVTK_INSTALL_LIBRARY_DIR:PATH=lib/paraview \\\
        -DVTK_USE_SYSTEM_DIY2=OFF \\\
        -DVTK_USE_SYSTEM_ICET=OFF \\\
        -DVTK_USE_SYSTEM_MPI4PY:BOOL=ON \\\
        -DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON \\\
        -DQtTesting_INSTALL_LIB_DIR=lib/paraview \\\
        -DQtTesting_INSTALL_CMAKE_DIR=lib/paraview/CMake \\\
        -DPARAVIEW_USE_MPI:BOOL=ON \\\
        -DICET_BUILD_TESTING:BOOL=ON \\\
        %{paraview_cmake_options}

%description
ParaView is an application designed with the need to visualize large data
sets in mind. The goals of the ParaView project include the following:

    * Develop an open-source, multi-platform visualization application.
    * Support distributed computation models to process large data sets.
    * Create an open, flexible, and intuitive user interface.
    * Develop an extensible architecture based on open standards.

ParaView runs on distributed and shared memory parallel as well as single
processor systems and has been successfully tested on Windows, Linux and
various Unix workstations and clusters. Under the hood, ParaView uses the
Visualization Toolkit as the data processing and rendering engine and has a
user interface written using a unique blend of Tcl/Tk and C++.

NOTE: The version in this package has NOT been compiled with MPI support.
%if %{build_openmpi}
Install the paraview-openmpi package to get a version compiled with openmpi.
%endif
%if %{build_mpich}
Install the paraview-mpich package to get a version compiled with mpich.
%endif


%package        data
Summary:        Data files for ParaView

Requires:       %{name} = %{version}-%{release}

BuildArch:      noarch

%description    data
%{summary}.


%package        devel
Summary:        Development files for %{name}

Requires:       %{name}%{?_isa} = %{version}-%{release}
Requires:       vtk-devel%{?_isa}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        doc
Summary:        Documentation files for ParaView

BuildRequires:  doxygen
BuildRequires:  graphviz
BuildRequires:  hardlink
BuildRequires:  python2-devel
%if 0%{?rhel} && 0%{?rhel} <= 7
BuildRequires:  numpy
BuildRequires:  python-sphinx
BuildRequires:  python-twisted-core
%else
BuildRequires:  python2-autobahn
BuildRequires:  python2-numpy
BuildRequires:  python2-sphinx
BuildRequires:  python2-twisted
%endif

BuildArch:      noarch

%description    doc
%{summary}.


%if %{build_openmpi}
%package        openmpi
Summary:        Parallel visualization application

BuildRequires:  openmpi-devel
BuildRequires:  mpi4py-openmpi
BuildRequires:  netcdf-openmpi-devel

Requires:       %{name}-data = %{version}-%{release}
Requires:       mpi4py-openmpi
Requires:       python-pygments
Requires:       python-six
Requires:       python2-autobahn
Requires:       python2-numpy
Requires:       python2-twisted

Obsoletes:      %{name}-mpi < 3.6.2-5

Provides:       %{name}-mpi = %{version}-%{release}

%description    openmpi
This package contains copies of the ParaView server binaries compiled with
OpenMPI.  These are named pvserver_openmpi, pvbatch_openmpi, etc.

You will need to load the openmpi-%{_arch} module to setup your path properly.


%package        openmpi-devel
Summary:        Development files for %{name}-openmpi

Requires:       %{name}-openmpi%{?_isa} = %{version}-%{release}

%description    openmpi-devel
The %{name}-openmpi-devel package contains libraries and header files for
developing applications that use %{name}-openmpi.
%endif


%if %{build_mpich}
%package        mpich
Summary:        Parallel visualization application

BuildRequires:  mpich-devel
BuildRequires:  mpi4py-mpich
BuildRequires:  netcdf-mpich-devel

Requires:       %{name}-data = %{version}-%{release}
Requires:       mpi4py-mpich
Requires:       python-pygments
Requires:       python-six
Requires:       python2-autobahn
Requires:       python2-numpy
Requires:       python2-twisted

Obsoletes:      %{name}-mpich2 < 3.98.1-6

%description    mpich
This package contains copies of the ParaView server binaries compiled with
mpich.  These are named pvserver_mpich, pvbatch_mpich, etc.

You will need to load the mpich-%{_arch} module to setup your path properly.


%package        mpich-devel
Summary:        Development files for %{name}-mpich

Requires:       %{name}-mpich%{?_isa} = %{version}-%{release}

Obsoletes:      %{name}-mpich2-devel < 3.98.1-6

Provides:       %{name}-mpich2-devel = %{version}-%{release}

%description    mpich-devel
The %{name}-mpich-devel package contains libraries and header files for
developing applications that use %{name}-mpich.
%endif


%prep
%setup -q -n ParaView-v%{version}%{?rcver:-%rcver}
# Install python properly
sed -i -s '/VTK_INSTALL_PYTHON_USING_CMAKE/s/TRUE/FALSE/' CMakeLists.txt
#Remove included thirdparty sources just to be sure
for x in vtkcgns %{?_with_protobuf:vtkprotobuf} vtkpygments
do
  rm -r ThirdParty/*/${x}
done
%if %{system_pugixml}
rm ThirdParty/pugixml/pugixml.*
%endif
for x in vtkexpat vtkfreetype %{?_with_gl2ps:vtkgl2ps} vtkhdf5 vtkjpeg vtklibxml2 vtklz4 vtkmpi4py vtknetcdf{,cpp} vtkoggtheora vtkpng vtksqlite vtktiff vtkTwisted vtkzlib vtkZopeInterface
do
  rm -r VTK/ThirdParty/*/${x}
done
%if 0%{?fedora} || 0%{?rhel} >= 8
rm -r VTK/ThirdParty/*/autobahn
%endif
# jsoncpp
%if 0%{system_jsoncpp}
rm -r VTK/ThirdParty/jsoncpp/vtkjsoncpp
%endif
# Remove unused KWSys items
find VTK/Utilities/KWSys/vtksys/ -name \*.[ch]\* | grep -vE '^VTK/Utilities/KWSys/vtksys/([a-z].*|Configure|SharedForward|String\.hxx|Base64|CommandLineArguments|Directory|DynamicLoader|Encoding|FStream|FundamentalType|Glob|MD5|Process|RegularExpression|System|SystemInformation|SystemTools)(C|CXX|UNIX)?\.' | xargs rm
# Work around gcc 4.9.0 regression
# https://gcc.gnu.org/bugzilla/show_bug.cgi?id=61294
sed -i -e 's/-Wl,--fatal-warnings//' VTK/CMake/vtkCompilerExtras.cmake
# We want to build with a system vtk someday, but it doesn't work yet
#rm -r VTK


%build
mkdir %{_target_platform}
pushd %{_target_platform}
%cmake3 .. \
        -DBUILD_DOCUMENTATION:BOOL=ON \
        -DVTK_INSTALL_INCLUDE_DIR:PATH=include/paraview \
        -DVTK_INSTALL_ARCHIVE_DIR:PATH=%{_lib}/paraview \
        -DVTK_INSTALL_LIBRARY_DIR:PATH=%{_lib}/paraview \
        -DPARAVIEW_INSTALL_DEVELOPMENT_FILES:BOOL=ON \
        -DQtTesting_INSTALL_LIB_DIR=%{_lib}/paraview \
        -DQtTesting_INSTALL_CMAKE_DIR=%{_lib}/paraview/CMake \
        %{paraview_cmake_options}
%make_build
#export LD_LIBRARY_PATH="%{buildroot}%{_libdir}:%{_libdir}"
#export PYTHONPATH="%{buildroot}%{_libdir}/%{name}/site-packages:${PYTHONPATH}"
#export PYTHONPATH="${PYTHONPATH%:}:%{python2_sitearch}/mpich"
export LANG=en_US.UTF-8
%make_build DoxygenDoc ParaViewDoc
#unset LD_LIBRARY_PATH
#unset PYTHONPATH
popd
%if %{build_openmpi}
mkdir %{_target_platform}-openmpi
pushd %{_target_platform}-openmpi
%{_openmpi_load}
%cmake3 .. \
        %{paraview_cmake_mpi_options}
# Fixup forward paths
sed -i -e 's,../%{_lib}/openmpi,..,' `find -name \*-forward.c`
%make_build
%{_openmpi_unload}
popd
%endif
%if %{build_mpich}
mkdir %{_target_platform}-mpich
pushd %{_target_platform}-mpich
%{_mpich_load}
# EL7 mpich module doesn't set PYTHONPATH
# https://bugzilla.redhat.com/show_bug.cgi?id=1148992
[ -z "$PYTHONPATH" ] && export PYTHONPATH=$MPI_PYTHON_SITEARCH
%cmake3 .. \
        %{paraview_cmake_mpi_options}
# Fixup forward paths
sed -i -e 's,../%{_lib}/mpich,..,' `find -name \*-forward.c`
%make_build
%{_mpich_unload}
popd
%endif


%install
# Fix permissions
find . \( -name \*.txt -o -name \*.xml -o -name '*.[ch]' -o -name '*.[ch][px][px]' \) -print0 | xargs -0 chmod -x

# Create some needed directories
install -d %{buildroot}%{_datadir}/applications
install -d %{buildroot}%{_datadir}/mime/packages
install -m644 %SOURCE1 %{buildroot}%{_datadir}/mime/packages

%if %{build_openmpi}
# Install openmpi version
%make_install -C %{_target_platform}-openmpi


#Remove mpi copy of doc and man pages and  data
rm -rf %{buildroot}%{_libdir}/openmpi/share/{appdata,applications,doc,icons,man,paraview}
%endif

%if %{build_mpich}
# Install mpich version
%make_install -C %{_target_platform}-mpich

#Remove mpi copy of doc and man pages and data
rm -rf %{buildroot}%{_libdir}/mpich/share/{appdata,applications,doc,icons,man,paraview}
%endif

#Install the normal version
%make_install -C %{_target_platform}

desktop-file-validate %{buildroot}%{_datadir}/applications/paraview.desktop
%if 0%{?fedora} || 0%{?rhel} >= 8
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml
%endif

#Cleanup only vtk conflicting binaries
rm %{buildroot}%{_bindir}/vtk{EncodeString,HashSource,LegacyColorMapXMLToJSON,ParseJava,Wrap{Hierarchy,Java,Python,Tcl}}*
rm -f %{buildroot}%{_bindir}/vtkParseOGLExt

# Strip build dir from VTKConfig.cmake (bug #917425)
find %{buildroot} -name VTKConfig.cmake | xargs sed -i -e '/builddir/s/^/#/'

# Build autodocs and move documentation-files to proper location
mkdir -p %{buildroot}%{_pkgdocdir}
install -pm 0644 README.md %{buildroot}%{_pkgdocdir}
mv %{buildroot}%{_docdir}/paraview-%{pv_majmin}/* %{buildroot}%{_pkgdocdir}
rm -rf %{buildroot}%{_docdir}/paraview-%{pv_majmin}
find %{buildroot}%{_pkgdocdir} -name '.*' -print0 | xargs -0 rm -frv
find %{buildroot}%{_pkgdocdir} -name '*.map' -or -name '*.md5' -print -delete
hardlink -cfv %{buildroot}%{_pkgdocdir}


%post
update-desktop-database &> /dev/null ||:

%postun
update-desktop-database &> /dev/null ||:

%pre
#Handle changing from directory to file
if [ -d %{_libdir}/paraview/paraview ]; then
  rm -r %{_libdir}/paraview/paraview
fi


%post data
/bin/touch --no-create %{_datadir}/mime/packages &>/dev/null || :
/bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null || :

%postun data
if [ $1 -eq 0 ] ; then
  update-mime-database %{_datadir}/mime &> /dev/null || :
  /bin/touch --no-create %{_datadir}/icons/hicolor &>/dev/null
  /usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
fi

%posttrans data
update-mime-database \
%if 0%{?fedora} || 0%{?rhel} >= 8
-n \
%endif
%{_datadir}/mime &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :


%files
%license Copyright.txt License_v1.2.txt
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README.md
%{_bindir}/paraview
%{_bindir}/pvbatch
# Currently disabled upstream
#{_bindir}/pvblot
%{_bindir}/pvdataserver
%{_bindir}/pvpython
%{_bindir}/pvrenderserver
%{_bindir}/pvserver
%{_bindir}/smTestDriver
%{_libdir}/paraview/

%files data
%{_datadir}/appdata/paraview.appdata.xml
%{_datadir}/applications/*paraview.desktop
%{_datadir}/icons/hicolor/*/apps/paraview.png
%{_datadir}/mime/packages/paraview.xml

%files devel
%{_bindir}/paraview-config
%{_bindir}/vtkWrapClientServer
%{_bindir}/vtkkwProcessXML
%{_includedir}/paraview/
%{_datadir}/cmake/

%files doc
%license %{_datadir}/licenses/%{name}*
%doc %{_pkgdocdir}


%if %{build_openmpi}
%files openmpi
%license %{_datadir}/licenses/%{name}*
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README.md
%{_libdir}/openmpi/bin/[ps]*
%{_libdir}/openmpi/lib/paraview/

%files openmpi-devel
%{_libdir}/openmpi/bin/vtk*
%{_libdir}/openmpi/include/paraview/
%{_libdir}/openmpi/share/cmake/
%endif


%if %{build_mpich}
%files mpich
%license %{_datadir}/licenses/%{name}*
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README.md
%{_libdir}/mpich/bin/[ps]*
%{_libdir}/mpich/lib/paraview/

%files mpich-devel
%{_libdir}/mpich/bin/vtk*
%{_libdir}/mpich/include/paraview/
%{_libdir}/mpich/share/cmake/
%endif


%changelog
* Fri Jun 16 2017 Orion Poplawski <orion@cora.nwra.com> - 5.4.0-1
- Update to 5.4.0

* Mon Apr 10 2017 Orion Poplawski <orion@cora.nwra.com> - 5.3.0-2
- Build with Qt5 on Fedora 26+ (bug #1437858)
- Drop old cmake config options

* Mon Mar 13 2017 Orion Poplawski <orion@cora.nwra.com> - 5.3.0-1
- Update to 5.3.0

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 5.2.0-5.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Thu Jan 26 2017 Orion Poplawski <orion@cora.nwra.com> - 5.2.0-5
- Rebuild with system protobuf 3.2.0

* Tue Jan 10 2017 Orion Poplawski <orion@cora.nwra.com> - 5.2.0-4
- Filter bundled protobuf from requires if needed

* Sun Jan 8 2017 Orion Poplawski <orion@cora.nwra.com> - 5.2.0-3
- Use bundled protobuf for now

* Wed Dec 28 2016 Rich Mattes <richmattes@gmail.com> - 5.2.0-2
- Rebuild for eigen3-3.3.1

* Sat Nov 19 2016 Orion Poplawski <orion@cora.nwra.com> - 5.2.0-1.1
- Rebuild for protobuf 3.1.0

* Thu Nov 17 2016 Orion Poplawski <orion@cora.nwra.com> - 5.2.0-1
- Update to 5.2.0 final

* Mon Nov 7 2016 Orion Poplawski <orion@cora.nwra.com> - 5.2.0-0.8.RC4
- Update to 5.2.0-RC4

* Fri Nov 4 2016 Orion Poplawski <orion@cora.nwra.com> - 5.2.0-0.7.RC3
- Build with bundled gl2ps

* Sat Oct 29 2016 Orion Poplawski <orion@cora.nwra.com> - 5.2.0-0.7.RC3
- Update to 5.2.0-RC3
- Drop libjsoncpp patch applied upstream

* Fri Oct 21 2016 Björn Esser <fedora@besser82.io> - 5.2.0-0.6.RC2
- Add needed (Build)Requires
- Remove cluttering files from %%{_pkgdocdir}

* Wed Oct 19 2016 Björn Esser <fedora@besser82.io> - 5.2.0-0.5.RC2
- Add needed Requires
- Reintroduce doc-subpkg
- Use unified %%{_pkgdocdir} and unified %%license
- Build documentation
- Proper Obsoletes versioning
- Spec-file improvements

* Wed Oct 19 2016 Björn Esser <fedora@besser82.io> - 5.2.0-0.4.RC2
- Drop obsolete stuff
- Use up-to-date macros
- Use semantic build-tree sub-dirs: 's!fedora!%%{_target_platform}!'

* Tue Oct 18 2016 Björn Esser <fedora@besser82.io> - 5.2.0-0.3.RC2
- Update to 5.2.0-RC2
- Drop patches merged by upstream
- Update libjsoncpp_so_11.patch

* Tue Oct 18 2016 Orion Poplawski <orion@cora.nwra.com> - 5.2.0-0.2.RC1
- Drop unneeded data dir
- Update bundled lib cleanup
- Do not use -f with rm to detect changes

* Mon Oct 17 2016 Björn Esser <fedora@besser82.io> - 5.2.0-0.1.RC1
- Update to 5.2.0-RC1
- Drop patches merged by upstream
- Add libjsoncpp_so_11.patch
- Create data-dir, if not created by `%make_install`
- Drop %%clean-section
- Clean trailing whitespaces

* Mon Oct 03 2016 Björn Esser <fedora@besser82.io> - 5.1.2-2
- Rebuilt for libjsoncpp.so.11

* Fri Sep 16 2016 Orion Poplawski <orion@cora.nwra.com> - 5.1.2-1
- Add upstream fix to not ship libFmmMesh.a
- Use cmake3 and %%cmake3 for EPEL compatibility

* Wed Aug 10 2016 Orion Poplawski <orion@cora.nwra.com> - 5.1.2-1
- Update to 5.1.2
- Use CMAKE_PREFIX_PATH to find mpi versions of libraries
- Ship installed static libraries, they are needed (bug #1304881)

* Wed Jun 29 2016 Orion Poplawski <orion@cora.nwra.com> - 5.1.0-1.1
- Rebuild for hdf5 1.8.17

* Mon Jun 20 2016 Orion Poplawski <orion@cora.nwra.com> - 5.1.0-1
- Update to 5.1.0
- Drop vtk-gcc6 patch fixed upstream
- Note more bundled libraries

* Mon Mar 28 2016 Orion Poplawski <orion@cora.nwra.com> - 5.0.1-1
- Update to 5.0.1 final

* Fri Mar 25 2016 Björn Esser <fedora@besser82.io> - 5.0.1-0.3.RC2
- Update to 5.0.1-RC2
- Drop Patch1 (paraview-lz4), applied upstream
- Use %%license and %%doc properly

* Fri Mar 25 2016 Björn Esser <fedora@besser82.io> - 5.0.1-0.2.RC1
- Rebuilt for libjsoncpp.so.1

* Thu Mar 3 2016 Orion Poplawski <orion@cora.nwra.com> - 5.0.1-0.1.RC1
- Update to 5.0.1-RC1
- Drop paraview-gcc6 patch applied upstream

* Mon Feb 1 2016 Orion Poplawski <orion@cora.nwra.com> - 5.0.0-1
- Update to 5.0.0 final
- Drop non_x86 patch, fixed upstream
- Add vtk-gcc6, paraview-gcc6 patches to support gcc6

* Fri Jan 22 2016 Orion Poplawski <orion@cora.nwra.com> - 5.0.0-0.6.RC3
- Rebuild for netcdf 4.4.0

* Fri Jan 15 2016 Jonathan Wakely <jwakely@redhat.com> - 5.0.0-0.5.RC3
- Rebuilt for Boost 1.60

* Thu Jan 7 2016 Orion Poplawski <orion@cora.nwra.com> - 5.0.0-0.4.RC3
- Validate appdata

* Tue Jan 5 2016 Orion Poplawski <orion@cora.nwra.com> - 5.0.0-0.3.RC3
- Update to 5.0.0-RC3
- Add patch to fix build on non-x86 systems
- Add patch to fix jsoncpp usage on ARM

* Fri Dec 18 2015 Orion Poplawski <orion@cora.nwra.com> - 5.0.0-0.2.RC2
- Update to 5.0.0-RC2
- Drop jsoncpp patch applied upstream

* Thu Dec 10 2015 Orion Poplawski <orion@cora.nwra.com> - 5.0.0-0.1.RC1
- Update to 5.0.0-RC1

* Thu Oct 29 2015 Orion Poplawski <orion@cora.nwra.com> - 4.4.0-2
- No longer set MPI_COMPILER as it is no longer needed and breaks with cmake
  3.4.0

* Fri Sep 18 2015 Orion Poplawski <orion@cora.nwra.com> - 4.4.0-1
- Update to 4.4.0
- Drop type, netcdf, and topological-sort-cmake patches applied upstream
- Use system eigen3, python-pygments, python-six (bug #1251289)
- Use bundled jsoncpp for F23 or earlier

* Thu Sep 17 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-15
- Rebuild for openmpi 1.10.0
- Add patch for jsoncpp 0.10 support

* Thu Aug 27 2015 Jonathan Wakely <jwakely@redhat.com> - 4.3.1-14
- Rebuilt for Boost 1.59

* Sat Aug 22 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-13
- Note bundled kwsys, remove unused kwsys files

* Wed Aug 19 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-12
- Do not ship static libraries

* Mon Aug 17 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-11
- Filter provides/requires to exclude private libraries

* Fri Aug 14 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-10
- Add patch for protobuf 2.6 support (fixes FTBFS bug #1239759)

* Mon Aug 10 2015 Sandro Mani <manisandro@gmail.com> - 4.3.1-9
- Rebuild for RPM MPI Requires Provides Change

* Wed Jul 29 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-8
- Rebuilt for https://fedoraproject.org/wiki/Changes/F23Boost159

* Wed Jul 22 2015 David Tardon <dtardon@redhat.com> - 4.3.1-7
- rebuild for Boost 1.58

* Fri Jul 10 2015 Jason L Tibbitts III <tibbs@math.uh.edu> - 4.3.1-6
- Add Exec= line to the desktop file (bug #1242012)

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Thu Apr 30 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-4
- Use upstream desktop file (bug #1216255)

* Wed Apr 29 2015 Kalev Lember <kalevlember@gmail.com> - 4.3.1-3
- Rebuilt for protobuf soname bump

* Wed Feb 04 2015 Petr Machata <pmachata@redhat.com> - 4.3.1-2
- Bump for rebuild.

* Tue Jan 27 2015 Orion Poplawski <orion@cora.nwra.com> - 4.3.1-1
- Update to 4.3.1

* Tue Jan 27 2015 Petr Machata <pmachata@redhat.com> - 4.2.0-3
- Rebuild for boost 1.57.0

* Thu Jan 8 2015 Orion Poplawski <orion@cora.nwra.com> - 4.2.0-2
- Rebuild for hdf 1.8.14
- Add patch to fix compilation error

* Wed Oct 1 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.0-1
- Update to 4.2.0 final

* Thu Sep 18 2014 Orion Poplawski <orion@cora.nwra.com> - 4.2.0-0.1.rc1
- Update to 4.2.0-RC1
- Drop paraview-install, paraview-4.0.1-Protobuf, and paraview-pqViewFrameActionGroup
  patches fixed upstream
- Build against system pugixml

* Mon Sep 08 2014 Rex Dieter <rdieter@fedoraproject.org> 4.1.0-9
- update scriptlets

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Mon Jul 21 2014 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-7
- Install missing headers (bug #1100911)
- Install TopologicalSort.cmake (bug #1116521)
- Adjust ParaViewPlugins.cmake for Fedora packaging (bug #118520)

* Tue Jun 10 2014 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-6
- Rebuild for hdf 1.8.13

* Fri Jun 06 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 4.1.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri May 23 2014 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-3
- Install missing pqViewFrameActionGroup.h header (bug #1100905)

* Thu May 22 2014 Petr Machata <pmachata@redhat.com> - 4.1.0-3
- Rebuild for boost 1.55.0

* Mon Feb 24 2014 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-2
- Rebuild for mpich-3.1

* Tue Jan 21 2014 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-1
- Update to 4.1.0 final
- Drop cstddef patch applied upstream

* Mon Dec 30 2013 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.1.rc2
- Rebase install patch
- Add patch to include needed cstddef for gcc 4.8.2
- Set VTK_INSTALL_DATA_DIR
- Set QtTesting_* install macros

* Fri Dec 27 2013 Orion Poplawski <orion@cora.nwra.com> - 4.1.0-0.1.rc2
- Update to 4.1.0-RC2

* Fri Oct 18 2013 Orion Poplawski <orion@cora.nwra.com> - 4.0.1-3
- Require vtk-devel for vtkProcessShader

* Mon Oct 14 2013 Orion Poplawski <orion@cora.nwra.com> - 4.0.1-2
- Remove conflicts with vtk-devel (bug #1018432)

* Mon Aug 12 2013 Orion Poplawski <orion@cora.nwra.com> - 4.0.1-1
- Update to 4.0.1
- Drop jpeg patch fixed upstream

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.98.1-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 30 2013 Petr Machata <pmachata@redhat.com> - 3.98.1-7
- Rebuild for boost 1.54.0

* Sat Jul 20 2013 Deji Akingunola <dakingun@gmail.com> - 3.98.1-6
- Rename mpich2 sub-packages to mpich and rebuild for mpich-3.0

* Thu May 16 2013 Orion Poplawski <orion@cora.nwra.com> - 3.98.1-5
- Rebuild for hdf5 1.8.11

* Tue Apr 30 2013 Jon Ciesla <limburgher@gmail.com> - 3.98.1-4
- Drop desktop vendor tag.

* Thu Mar 7 2013 Orion Poplawski <orion@cora.nwra.com> - 3.98.1-3
- Remove builddir path from VTKConfig.cmake (bug #917425)

* Sun Feb 24 2013 Orion Poplawski <orion@cora.nwra.com> - 3.98.1-2
- Remove only vtk conflicting binaries (bug #915116)
- Do not move python libraries

* Wed Feb 20 2013 Orion Poplawski <orion@cora.nwra.com> - 3.98.1-1
- Update to 3.98.1
- Drop pvblot patch
- Add upstream patch to fix jpeg_mem_src support

* Mon Jan 28 2013 Orion Poplawski <orion@cora.nwra.com> - 3.98.0-3
- Drop kwProcessXML patch, leave as vtkkwProcessXML with rpath

* Mon Jan 21 2013 Adam Tkac <atkac redhat com> - 3.98.0-2
- rebuild due to "jpeg8-ABI" feature drop

* Mon Dec 17 2012 Orion Poplawski <orion@cora.nwra.com> - 3.98.0-1
- Update to 3.98.0
- Remove source of more bundled libraries
- Drop include, gcc47, vtkboost, and hdf5 patches
- Rebase kwprocessxml_rpath and system library patches
- Add patch to fix install locations
- Add patch to use system protobuf
- Add BR gl2ps-devel >= 1.3.8
- Disable pvblot for now
- Build with hdf5 1.8.10

* Thu Nov 1 2012 Orion Poplawski <orion@cora.nwra.com> - 3.14.1-5
- Rebuild for mpich2 1.5
- Add patch to compile with current boost

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.14.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Jun 13 2012 Orion Poplawski <orion@cora.nwra.com> - 3.14.1-3
- Don't ship vtkWrapHierarchy, conflicts with vtk (Bug 831834)

* Tue May 15 2012 Orion Poplawski <orion@cora.nwra.com> - 3.14.1-2
- Rebuild with hdf5 1.8.9

* Mon Apr 9 2012 Orion Poplawski <orion@cora.nwra.com> - 3.14.1-1
- Update to 3.14.1
- Add BR hwloc-devel

* Tue Apr 3 2012 Orion Poplawski <orion@cora.nwra.com> - 3.14.0-4
- Add patch to buid kwProcessXML as a forwarded executable (bug #808490)

* Thu Mar 29 2012 Orion Poplawski <orion@cora.nwra.com> - 3.14.0-3
- Only remove vtk conflicting binaries (bug #807756)

* Wed Feb 29 2012 Orion Poplawski <orion@cora.nwra.com> - 3.14.0-2
- Add patch to make vtk use system libraries

* Wed Feb 29 2012 Orion Poplawski <orion@cora.nwra.com> - 3.14.0-1
- Update to 3.14.0
- Rebase gcc47 patch
- Try to handle python install problems manually

* Tue Feb 28 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.12.0-8
- Rebuilt for c++ ABI breakage

* Thu Jan 26 2012 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-7
- Build with gcc 4.7
- Add patch to support gcc 4.7
- Build with new libOSMesa

* Tue Dec 27 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-6
- vtkPV*Python.so needs to go into the paraview python dir
- Drop chrpath

* Fri Dec 16 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-5
- Oops, install vtk*Python.so, not libvtk*Python.so

* Mon Dec 12 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-4
- Install more libvtk libraries by hand and manually remove rpath

* Fri Dec 9 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-3
- Add patch from Petr Machata to build with boost 1.48.0

* Thu Dec 1 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-2
- Enable PARAVIEW_INSTALL_DEVELOPMENT and re-add -devel sub-package
- Install libvtk*Python.so by hand for now

* Thu Nov 10 2011 Orion Poplawski <orion@cora.nwra.com> - 3.12.0-1
- Update to 3.12.0

* Fri Oct 28 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-6
- Fixup forward paths for mpi versions (bug #748221)

* Thu Jun 23 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-5
- Add BR qtwebkit-devel, fixes FTBS bug 716151

* Tue May 17 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-4
- Rebuild for hdf5 1.8.7

* Tue Apr 19 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-3
- No need to move python install with 3.10.1

* Tue Apr 19 2011 Dan Horák <dan[at]danny.cz> - 3.10.1-2
- no openmpi on s390(x)

* Mon Apr 18 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.1-1
- Update to 3.10.1
- Drop build patch fixed upstream

* Mon Apr 4 2011 Orion Poplawski <orion@cora.nwra.com> - 3.10.0-1
- Update to 3.10.0
- Drop lib and py27 patches fixed upstream
- Add patch for gcc 4.6.0 support
- Update system hdf5 handling
- Cleanup unused build options
- Build more plugins

* Tue Mar 29 2011 Deji Akingunola <dakingun@gmail.com> - 3.8.1-5
- Rebuild for mpich2 soname bump

* Wed Oct 20 2010 Adam Jackson <ajax@redhat.com> 3.8.1-4
- Rebuild for new libOSMesa soname

* Thu Oct 7 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.1-3
- Remove any previous %%{_libdir}/paraview/paraview directories
  which prevent updates

* Tue Oct 5 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.1-2
- Disable install of third party libraries

* Fri Oct 1 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.1-1
- Update to 3.8.1
- Drop devel sub-package
- Drop installpath patch
- Drop hdf5-1.8 patch, build with hdf5 1.8 API
- Cleanup build

* Fri Jul 30 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.0-4
- Add patch to support python 2.7

* Tue Jul 27 2010 David Malcolm <dmalcolm@redhat.com> - 3.8.0-3
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Fri Jun 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.0-2
- Drop doc sub-package

* Tue Jun 1 2010 Orion Poplawski <orion@cora.nwra.com> - 3.8.0-1
- Update to 3.8.0
- Update demo patch
- Update hdf5 patch
- Drop old documentation patches
- Add patch to add needed include headers
- Add patch from upstream to fix install path issue

* Sat Mar 13 2010 Kevin Kofler <Kevin@tigcc.ticalc.org> - 3.6.2-4
- BR qt-assistant-adp-devel
- Don't Require qt4-assistant, should be qt-assistant-adp now, and it (or qt-x11
  4.6.x which Provides it) gets dragged in anyway by the soname dependencies

* Fri Feb 19 2010 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-3
- More MPI packaging changes

* Tue Feb 16 2010 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-2
- Conform to updated MPI packaging guidelines
- Build mpich2 version

* Mon Jan 4 2010 Orion Poplawski <orion@cora.nwra.com> - 3.6.2-1
- Update to 3.6.2

* Thu Nov 19 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-7
- New location for openmpi (fixes FTBFS bug #539179)

* Mon Aug 31 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-6
- Don't ship lproj, conflicts with vtk

* Thu Aug 27 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-5
- Specify PV_INSTALL_LIB_DIR as relative path, drop install prefix patch
- Update assitant patch to use assistant_adp, don't ship assistant-real

* Wed Aug 26 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-4
- Disable building various plugins that need OverView

* Tue Aug 25 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-3
- Disable building OverView - not ready yet

* Fri Aug 21 2009 Tomas Mraz <tmraz@redhat.com> - 3.6.1-2
- rebuilt with new openssl

* Wed Jul 22 2009 Orion Poplawski <orion@cora.nwra.com> - 3.6.1-1
- Update to 3.6.1

* Thu May 7 2009 Orion Poplawski <orion@cora.nwra.com> - 3.4.0-5
- Update doc patch to look for help file in the right place (bug #499273)

* Tue Feb 24 2009 Orion Poplawski <orion@cora.nwra.com> - 3.4.0-4
- Rebuild with hdf5 1.8.2, gcc 4.4.0
- Update hdf5-1.8 patch to work with hdf5 1.8.2
- Add patch to allow build with Qt 4.5
- Move documentation into noarch sub-package

* Sat Jan 17 2009 Tomas Mraz <tmraz@redhat.com> - 3.4.0-3
- rebuild with new openssl

* Sun Nov 30 2008 Ignacio Vazquez-Abrams <ivazqueznet+rpm@gmail.com> - 3.4.0-2
- Rebuild for Python 2.6

* Fri Oct 17 2008 Orion Poplawski <orion@cora.nwra.com> - 3.4.0-1
- Update to 3.4.0 final

* Thu Oct 2 2008 Orion Poplawski <orion@cora.nwra.com> - 3.4.0-0.20081002.1
- Update 3.4.0 CVS snapshot
- Update gcc43 patch
- Drop qt patch, upstream now allows compiling against Qt 4.4.*

* Mon Aug 11 2008 Orion Poplawski <orion@cora.nwra.com> - 3.3.1-0.20080811.1
- Update 3.3.1 CVS snapshot
- Update hdf5 patch to drop upstreamed changes
- Fix mpi build (bug #450598)
- Use rpath instead of ls.so conf files so mpi and non-mpi can be installed at
  the same time
- mpi package now just ships mpi versions of the server components
- Drop useless mpi-devel subpackage
- Update hdf5 patch to fix H5pubconf.h -> H5public.h usage

* Wed May 21 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.3.0-0.20080520.1
- Update to 3.3.0 CVS snapshot
- Update qt and gcc43 patches, drop unneeded patches
- Add openssl-devel, gnuplot, and wget BRs
- Update license text filename
- Set VTK_USE_RPATH to off, needed with development versions
- Run ctest in %%check - still need to exclude more tests

* Wed Mar 5 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-5
- Rebuild for hdf5 1.8.0 using compatability API define and new patch

* Mon Feb 18 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-4
- Add patch to compile with gcc 4.3

* Fri Jan 18 2008 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-3
- Add patch to fix parallel make
- Obsolete demos package (bug #428528)

* Tue Dec 18 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-2
- Name ld.so.conf.d file with .conf extension
- Drop parallel make for now

* Mon Dec 03 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.2.1-1
- Update to 3.2.1
- Use macros for version numbers
- Add patches to fix documentation install location and use assistant-qt4,
  not install copies of Qt libraries, and not use rpath.
- Install ld.so.conf.d file
- Fixup desktop files

* Thu Aug 23 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.0.2-2
- Update license tag to BSD
- Fix make %%{_smp_mflags}
- Rebuild for ppc32

* Wed Jul 11 2007 - Orion Poplawski <orion@cora.nwra.com> - 3.0.2-1
- Update to 3.0.2
- Turn mpi build back on
- Add devel packages
- Remove demo package no longer in upstream
- Use cmake macros

* Thu Mar 08 2007 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-6
- Don't build mpi version until upstream fixes the build system

* Fri Dec 22 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-5
- Fix .so permissions
- Patch for const issue
- Patch for new cmake
- Build with openmpi

* Thu Dec 14 2006 - Jef Spaleta <jspaleta@gmail.com> - 2.4.4-4
- Bump and build for python 2.5

* Fri Oct  6 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-3
- Install needed python libraries to get around make install bug

* Wed Oct  4 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-2
- Re-enable OSMESA support for FC6
- Enable python wrapping

* Fri Sep 15 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.4-1
- Update to 2.4.4

* Thu Jun 29 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-8
- No OSMesa support in FC5
- Make data sub-package pull in main package (bug #193837)
- A patch from CVS to fix vtkXOpenRenderWindow.cxx
- Need lam-devel for FC6

* Fri Apr 21 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-7
- Re-enable ppc

* Mon Apr 17 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-6
- Exclude ppc due to gcc bug #189160

* Wed Apr 12 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-5
- Cleanup permissions

* Mon Apr 10 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-4
- Add icon and cleanup desktop file

* Mon Apr 10 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-3
- Add VTK_USE_MANGLE_MESA for off screen rendering
- Cleanup source permisions
- Add an initial .desktop file
- Make requirement on -data specific to version
- Don't package Ice-T man pages and cmake files

* Thu Apr  6 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-2
- Add mpi version

* Tue Apr  4 2006 - Orion Poplawski <orion@cora.nwra.com> - 2.4.3-1
- Initial Fedora Extras version
