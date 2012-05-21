%define keepstatic 1

Name:       lua
Summary:    Powerful light-weight programming language
Version:    5.1.4
Release:    6
Group:      Development/Languages
License:    MIT
URL:        http://www.lua.org/
Source0:    http://www.lua.org/ftp/lua-%{version}.tar.gz
Patch0:     patch-lua-5.1.4-2
Patch1:     lua-5.1.4-autotoolize.patch
Patch2:     buildfix.patch
BuildRequires:  pkgconfig(ncurses)


%description
Lua is a powerful light-weight programming language designed for
extending applications. Lua is also frequently used as a
general-purpose, stand-alone language. Lua is free software.
Lua combines simple procedural syntax with powerful data description
constructs based on associative arrays and extensible semantics. Lua
is dynamically typed, interpreted from bytecodes, and has automatic
memory management with garbage collection, making it ideal for
configuration, scripting, and rapid prototyping.



%package -n liblua
Summary:    The Lua library
Group:      System/Libraries
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig

%description -n liblua
This package contains the shared version of liblua for %{name}.

%package -n liblua-static
Summary:    Static library for %{name}
Group:      Development/Libraries
Requires:   liblua-devel = %{version}-%{release}

%description -n liblua-static
This package contains the static version of liblua for %{name}.

%package -n liblua-devel
Summary:    Development files for %{name}
Group:      Development/Libraries
Requires:   liblua = %{version}-%{release}

%description -n liblua-devel
This package contains development files for %{name}.


%prep
%setup -q 

# patch-lua-5.1.4-2
%patch0 -p1
# lua-5.1.4-autotoolize.patch
%patch1 -p1
# buildfix.patch
%patch2 -p1

%build
# fix perms on auto files
chmod u+x autogen.sh config.guess config.sub configure depcomp install-sh missing

%configure  \
    --without-readline

make %{?jobs:-j%jobs}

sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
# hack so that only /usr/bin/lua gets linked with readline as it is the
# only one which needs this and otherwise we get License troubles
make %{?_smp_mflags} LIBS="-ldl" luac_LDADD="liblua.la -lm -ldl"
# also remove readline from lua.pc
sed -i 's/-lreadline -lncurses //g' etc/lua.pc



%install
rm -rf %{buildroot}
%make_install 

%remove_docs

%post -n liblua -p /sbin/ldconfig

%postun -n liblua -p /sbin/ldconfig

%files
%{_bindir}/lua*

%files -n liblua
%{_libdir}/liblua-*.so

%files -n liblua-static
%{_libdir}/*.a

%files -n liblua-devel
%{_includedir}/l*.h
%{_includedir}/l*.hpp
%{_libdir}/liblua.so
%{_libdir}/pkgconfig/*.pc

