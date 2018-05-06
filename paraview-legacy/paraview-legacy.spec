%ifarch s390 s390x
%global build_openmpi 0
%endif
%{!?build_openmpi:%global build_openmpi 1}
%{!?build_mpich:%global build_mpich 1}
%global pv_maj 5
%global pv_min 4
%global pv_patch 1
%global pv_majmin %{pv_maj}.%{pv_min}
#global rcsuf rc3
%{?rcsuf:%global relsuf .%{rcsuf}}
%{?rcsuf:%global versuf -%{rcsuf}}

# Python2 prefix for building on rhel
%if 0%{?rhel}
%global py2_prefix python
%else
%global py2_prefix python2
%endif

# VTK currently is carrying local modifications to gl2ps
%bcond_with gl2ps
%if !%{with gl2ps}
%global vtk_use_system_gl2ps -DVTK_USE_SYSTEM_GL2PS:BOOL=OFF
%endif

# Enable VisitBridge plugin (bz#1546474)
%bcond_without VisitBridge

# We need jsoncpp >= 0.7
%if 0%{?fedora} || 0%{?rhel} >= 8
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

Name:           paraview
Version:        %{pv_majmin}.%{pv_patch}
Release:        3%{?relsuf}%{?dist}
Summary:        Parallel visualization application

License:        BSD
URL:            https://www.paraview.org/
Source0:        https://www.paraview.org/files/v%{pv_majmin}/ParaView-v%{version}%{?versuf}.tar.gz
Source1:        https://raw.githubusercontent.com/mrklein/packages/master/paraview-legacy/paraview.xml

Patch0:         https://raw.githubusercontent.com/mrklein/packages/master/paraview-legacy/%{name}-%{version}-jsoncpp_184.patch
Patch1:         https://raw.githubusercontent.com/mrklein/packages/master/paraview-legacy/%{name}-%{version}-fix_VisItBridge_builderror.patch

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
BuildRequires:  %{py2_prefix}-devel, tk-devel, hdf5-devel
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

Requires: hdf5%{?_hdf5_version: = %{_hdf5_version}}
Requires: %{name}-data = %{version}-%{release}
Requires: %{py2_prefix}-pygments
Requires: %{py2_prefix}-six
%{?fedora:Requires: python2-numpy}
%{?rhel:Requires: numpy}
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires: numpy
Requires: python-twisted-core
%else
Requires: python2-autobahn
Requires: python2-numpy
Requires: python2-twisted
%endif
%if %{with protobuf}
Requires: protobuf
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
%if %{with protobuf}
%global __requires_exclude ^lib(IceT|QtTesting|vtk).*$
%else
%global __requires_exclude ^lib(IceT|QtTesting|vtk|protobuf).*$
%endif


#-- Plugin: VRPlugin - Virtual Reality Devices and Interactor styles : Disabled - Requires VRPN
#-- Plugin: MantaView - Manta Ray-Cast View : Disabled - Requires Manta
#-- Plugin: ForceTime - Override time requests : Disabled - Build is failing
#-- Plugin: VaporPlugin - Plugin to read NCAR VDR files : Disabled - Requires vapor

# We want to build with a system vtk someday, but it doesn't work yet
# -DUSE_EXTERNAL_VTK:BOOL=ON \\\
# -DVTK_DIR=%%{_libdir}/vtk \\\

%global paraview_cmake_options \\\
        -DCMAKE_BUILD_TYPE=RelWithDebInfo \\\
        -DTCL_LIBRARY:PATH=tcl \\\
        -DPARAVIEW_BUILD_PLUGIN_AdiosReader:BOOL=ON \\\
        -DPARAVIEW_BUILD_PLUGIN_EyeDomeLighting:BOOL=ON \\\
        -DPARAVIEW_ENABLE_PYTHON:BOOL=ON \\\
%if %{with VisitBridge} \
        -DPARAVIEW_USE_VISITBRIDGE=ON \\\
        -DVTK_USE_SYSTEM_VISITLIB:BOOL=OFF \\\
        -DVISIT_BUILD_READER_CGNS=ON \\\
%endif \
        -DPARAVIEW_WWW_DIR=%{buildroot}%{_pkgdocdir} \\\
        -DPYTHONQT_DIR=/usr \\\
        -DVTK_CUSTOM_LIBRARY_SUFFIX="" \\\
        -DVTK_INSTALL_DATA_DIR=share/paraview \\\
        -DVTK_INSTALL_PACKAGE_DIR=share/cmake/paraview \\\
        -DVTK_PYTHON_SETUP_ARGS="--prefix=/usr --root=%{buildroot}" \\\
        -DVTK_RENDERING_BACKEND:STRING=OpenGL \\\
        -DVTK_LEGACY_SILENT:BOOL=ON \\\
        -DVTK_USE_OGGTHEORA_ENCODER:BOOL=ON \\\
        -DVTK_USE_SYSTEM_LIBRARIES=ON \\\
        -DVTK_USE_SYSTEM_AUTOBAHN:BOOL=ON \\\
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
%if %{with VisitBridge} \
        -DPARAVIEW_USE_VISITBRIDGE=ON \\\
        -DVTK_USE_SYSTEM_VISITLIB:BOOL=OFF \\\
        -DVISIT_BUILD_READER_CGNS=ON \\\
%endif \
        %{paraview_cmake_options}

%description
ParaView is an open-source, multi-platform data analysis and visualization
application. ParaView users can quickly build visualizations to analyze their
data using qualitative and quantitative techniques. The data exploration can
be done interactively in 3D or programmatically using ParaView’s batch
processing capabilities.

ParaView was developed to analyze extremely large datasets using distributed
memory computing resources. It can be run on supercomputers to analyze
datasets of petascale size as well as on laptops for smaller data.

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
BuildRequires:  %{py2_prefix}-devel
%{?fedora:BuildRequires: python2-numpy}
%{?rhel:BuildRequires: numpy}
BuildRequires:  %{py2_prefix}-sphinx

# Unavailable on rhel
BuildRequires:  %{py2_prefix}-twisted
BuildRequires:  %{py2_prefix}-autobahn

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
Requires:       %{py2_prefix}-pygments
Requires:       %{py2_prefix}-six
%{?fedora:Requires: python2-numpy}
%{?rhel:Requires: numpy}
Requires:       %{py2_prefix}-twisted
Requires:       %{py2_prefix}-autobahn

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
Requires:       %{py2_prefix}-pygments
Requires:       %{py2_prefix}-six
%{?fedora:Requires: python2-numpy}
%{?rhel:Requires: numpy}
Requires:       %{py2_prefix}-twisted
Requires:       %{py2_prefix}-autobahn

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
%autosetup -n ParaView-v%{version}%{?versuf} -p 1

%if %{with VisitBridge}
cp -p Utilities/VisItBridge/README.md Utilities/VisItBridge/README-VisItBridge.md

# See https://gitlab.kitware.com/paraview/paraview/issues/17456
rm -f Utilities/VisItBridge/databases/readers/Vs/VsStaggeredField.C
%endif

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
for x in autobahn vtkexpat vtkfreetype %{?_with_gl2ps:vtkgl2ps} vtkhdf5 vtkjpeg vtklibxml2 vtklz4 vtkmpi4py vtknetcdf{,cpp} vtkoggtheora vtkpng vtksqlite vtktiff vtkTwisted vtkzlib vtkZopeInterface
do
  rm -r VTK/ThirdParty/*/${x}
done
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
%{_openmpi_load}

# Install openmpi version
%make_install -C %{_target_platform}-openmpi

#Remove mpi copy of doc and man pages and  data
rm -rf %{buildroot}%{_libdir}/openmpi/share/{appdata,applications,doc,icons,man,paraview}

# Fix Python2 script
sed -i "1 s|^#!/usr/bin/env python\b|#!%{__python2}|" %{buildroot}%{_libdir}/openmpi/lib/paraview/site-packages/vtk/web/launcher.py
chmod 0755 %{buildroot}$MPI_LIB/paraview/site-packages/vtk/web/launcher.py

# Fix shell script permissions
chmod 0755 %{buildroot}%{_libdir}/openmpi/share/cmake/paraview/pre-commit
%{_openmpi_unload}
%endif

%if %{build_mpich}
%{_mpich_load}

# Install mpich version
%make_install -C %{_target_platform}-mpich

#Remove mpi copy of doc and man pages and data
rm -rf %{buildroot}%{_libdir}/mpich/share/{appdata,applications,doc,icons,man,paraview}

# Fix Python2 script
sed -i "1 s|^#!/usr/bin/env python\b|#!%{__python2}|" %{buildroot}%{_libdir}/mpich/lib/paraview/site-packages/vtk/web/launcher.py
chmod 0755 %{buildroot}$MPI_LIB/paraview/site-packages/vtk/web/launcher.py

# Fix shell script permissions
chmod 0755 %{buildroot}%{_libdir}/mpich/share/cmake/paraview/pre-commit
%{_mpich_unload}
%endif

#Install the normal version
%make_install -C %{_target_platform}

desktop-file-validate %{buildroot}%{_datadir}/applications/paraview.desktop
%if 0%{?fedora} || 0%{?rhel} >= 8
appstream-util validate-relax --nonet %{buildroot}/%{_datadir}/appdata/*.appdata.xml
%endif

#Cleanup only vtk conflicting binaries
rm %{buildroot}%{_bindir}/vtk{EncodeString,HashSource,LegacyColorMapXMLToJSON,ParseJava,Wrap{Hierarchy,Java,Python,Tcl}}*

# Fix Python2 script
sed -i "1 s|^#!/usr/bin/env python\b|#!%{__python2}|" %{buildroot}%{_libdir}/paraview/site-packages/vtk/web/launcher.py
chmod 0755 %{buildroot}%{_libdir}/paraview/site-packages/vtk/web/launcher.py

# Fix shell script permissions
chmod 0755 %{buildroot}%{_datadir}/cmake/paraview/pre-commit

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

%if 0%{?rhel} && 0%{?rhel} <= 7
%post
update-desktop-database &> /dev/null ||:

%postun
update-desktop-database &> /dev/null ||:
%endif

%pre
#Handle changing from directory to file
if [ -d %{_libdir}/paraview/paraview ]; then
  rm -r %{_libdir}/paraview/paraview
fi

%if 0%{?rhel} && 0%{?rhel} <= 7
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
update-mime-database %{_datadir}/mime &> /dev/null || :
/usr/bin/gtk-update-icon-cache %{_datadir}/icons/hicolor &>/dev/null || :
%endif

%files
%license Copyright.txt License_v1.2.txt
%doc %dir %{_pkgdocdir}
%doc %{_pkgdocdir}/README.md
%doc Utilities/VisItBridge/README-VisItBridge.md
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
%doc Utilities/VisItBridge/README-VisItBridge.md
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
%doc Utilities/VisItBridge/README-VisItBridge.md
%{_libdir}/mpich/bin/[ps]*
%{_libdir}/mpich/lib/paraview/

%files mpich-devel
%{_libdir}/mpich/bin/vtk*
%{_libdir}/mpich/include/paraview/
%{_libdir}/mpich/share/cmake/
%endif


%changelog
* Sun May 06 2018 Alexey Matveichev <alexey@matveichev.com> - 5.4.1-3
- Fedora 28 SPEC file as a base
- Removed Qt5
- Adapted for legacy rendering engine
