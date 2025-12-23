{ #lib
 python3Packages
}:

python3Packages.buildPythonApplication rec {
    pname = "ctf-mgnt";
    version = "0.3.3";

    propagatedBuildInputs = [
        # List of dependencies
        python3Packages.configargparse
        python3Packages.netaddr
    ];


    pyproject = true;
    build-system = [ python3Packages.setuptools ];

    src = ./.;

    installPhase = ''
        install -Dm755 ${./${pname}.py} $out/bin/${pname}
    '';
}
