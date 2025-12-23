{ #lib
 python3Packages,
 setuptools
}:

python3Packages.buildPythonApplication rec {
    pname = "ctf-mgnt";
    version = "0.1.0";

    propagatedBuildInputs = [
        # List of dependencies
        python3Packages.configargparse
        python3Packages.netaddr
    ];


    pyproject = true;
    build-system = [ setuptools ];

    src = ./.;

    installPhase = ''
        install -Dm755 ${./${pname}.py} $out/bin/${pname}
    '';
}
