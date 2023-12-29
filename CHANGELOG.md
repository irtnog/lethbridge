# CHANGELOG



## v0.2.3 (2023-12-29)

### Documentation

* docs: remove extraneous code tag ([`2855c49`](https://github.com/irtnog/lethbridge/commit/2855c49e1896b23973577bef63efac75fd0e3658))

* docs: re-point the build status shield at the new CI workflow ([`cb1a53a`](https://github.com/irtnog/lethbridge/commit/cb1a53a7368e38240723efaaab831510d9684ab9))

### Fix

* fix(packaging): add missing project description ([`362cefc`](https://github.com/irtnog/lethbridge/commit/362cefc4cecb665b1e557c78419442f7bc77f550))


## v0.2.2 (2023-12-29)

### Build

* build: add missing apt-get verb ([`d71ca55`](https://github.com/irtnog/lethbridge/commit/d71ca557ed6c90b7fa27bc820fd7eaad64c5ebc4))

* build: simulate a database DROP when restoring SQLite backups ([`7e3f1c5`](https://github.com/irtnog/lethbridge/commit/7e3f1c5dfe515476b1945a803c553f180198c7fc))

* build: only back up the `lethbridge` database, same as the migration test fixtures ([`42f4952`](https://github.com/irtnog/lethbridge/commit/42f49522f54f83ae5faaf090cad22693c2fd04cc))

* build: run `docker exec` in interactive mode so I/O redirection works ([`fed7808`](https://github.com/irtnog/lethbridge/commit/fed7808c7d833931bb55738dfb4842e910290a37))

* build: fix indentation ([`4de9416`](https://github.com/irtnog/lethbridge/commit/4de9416c9f5219e9dee950a042e9ce94d9fa52ff))

* build: prevent virtual environment updates when running unrelated targets ([`5f872fa`](https://github.com/irtnog/lethbridge/commit/5f872faea5c4f840b8d8e38f4b213f6a90d7d291))

* build: pass arguments to pytest similar to Alembic ([`95c154e`](https://github.com/irtnog/lethbridge/commit/95c154e9e0844309c5bebe9b8c51833d2be6c215))

* build: only run migration test fixture targets if they don&#39;t already exist

Migration test fixtures should be write-once since they depend on the
code base at the time they&#39;re run.  Changes to dependencies shouldn&#39;t
regenerate them. ([`6641c80`](https://github.com/irtnog/lethbridge/commit/6641c8032c89fa3dc6de044c3f448167288fe475))

* build: generate migration test fixtures from the mock galaxy data ([`3a91cf5`](https://github.com/irtnog/lethbridge/commit/3a91cf501d257f6b6968c6b142925a4a2c693335))

* build: combine development database management with an Alembic command wrapper ([`55b6e1b`](https://github.com/irtnog/lethbridge/commit/55b6e1b404b90c44fbd16a3262e72ea14e7f61a1))

* build: sort imports in Alembic revision scripts ([`675d29f`](https://github.com/irtnog/lethbridge/commit/675d29f1160e331e47c456ddd16d029b6c9494f7))

* build: shorten/rename dependencies on psycopg2cffi compatibility target ([`ae61612`](https://github.com/irtnog/lethbridge/commit/ae6161256bd06658ff328ec9a8a5bd9758a81e61))

* build: have make manage the complete lifecycle of the development databases ([`0216751`](https://github.com/irtnog/lethbridge/commit/0216751da87deae8f2ae6c07cc9600ab5c2a0882))

* build: add a volume to the migration dev database to facilitate restores ([`2f7d7d2`](https://github.com/irtnog/lethbridge/commit/2f7d7d26fb8eae3577dad894505e447929f3ba5b))

* build: mark phony make targets to avoid inadvertent conflicts with real files/directories ([`efb71a1`](https://github.com/irtnog/lethbridge/commit/efb71a11cb3bd9016373d8728ce27837a17c26af))

* build: add bashbrew and manifest-tool to the development environment ([`e768765`](https://github.com/irtnog/lethbridge/commit/e76876557438c5130c98b25490c87244d1a8fe71))

* build: install or activate the development environment automatically in Emacs

This requires enabling
[`pyvenv-mode`](https://github.com/jorgenschaefer/pyvenv). ([`9b6eeec`](https://github.com/irtnog/lethbridge/commit/9b6eeec374dc8980cde62bf20f7a20f4a4558a6b))

### Ci

* ci: merge the ci and lint workflows ([`0dda3a0`](https://github.com/irtnog/lethbridge/commit/0dda3a02e11230131deaadef57c5d70d2cbbe0af))

* ci: re-enable automated releases ([`9201d83`](https://github.com/irtnog/lethbridge/commit/9201d83133c65edbfc67f0f9676c9b87b6da1ba2))

* ci: merge test and release workflows ([`76f5b8d`](https://github.com/irtnog/lethbridge/commit/76f5b8df0d4cbafafafc1f7990335937bf984c1f))

* ci: simplify linting ([`8e22c4d`](https://github.com/irtnog/lethbridge/commit/8e22c4d5b21fa0a311223aa8265e540ac726b0d9))

### Documentation

* docs: note isort&#39;s behavior ([`398ff66`](https://github.com/irtnog/lethbridge/commit/398ff66f3fa67e7a6bf3a2fb5b582a8e509d9adc))

* docs: emphasize the Alembic command wrapper&#39;s dependence on running/existing databases ([`a36f20a`](https://github.com/irtnog/lethbridge/commit/a36f20ab837c6d1e5776ea777fa2047c12570195))

* docs: update description ([`d16b6ec`](https://github.com/irtnog/lethbridge/commit/d16b6ecac2cfe9ef8931dd935c0834c48a84e8a8))

* docs: require tests for all code changes ([`ff76cd0`](https://github.com/irtnog/lethbridge/commit/ff76cd0542ef45aef807959f95ba326bcc7e6664))

* docs: include Docker in the project dependencies ([`5935013`](https://github.com/irtnog/lethbridge/commit/593501307999fea3441692618249ae8883460c17))

* docs: add parenthetical noting the same command also handles updates ([`4b2407f`](https://github.com/irtnog/lethbridge/commit/4b2407f860b7932a028e429ae91dd6d40edcbbd0))

* docs: note that the shorter test suite restricts itself to one database engine ([`a6f1778`](https://github.com/irtnog/lethbridge/commit/a6f177848cf139628d90c6d3da33e11d6d725bd2))

* docs: replace parenthetical with relative clause ([`1919234`](https://github.com/irtnog/lethbridge/commit/191923408f58aa2feb19637176baf709810b77cc))

* docs: show how to activate the virtual environment ([`81aaa35`](https://github.com/irtnog/lethbridge/commit/81aaa35460d9e89e0b09645fdd0f0f762c0cec82))

* docs: mention other make targets sooner ([`fa5989d`](https://github.com/irtnog/lethbridge/commit/fa5989d76d4108c072b5460f9edbea6e6c113a00))

* docs: emphasize changes covering multiple scopes, not just multiple packages ([`f42710f`](https://github.com/irtnog/lethbridge/commit/f42710f16b1e60cabd29ffd11aedb9361bf4642f))

* docs: add Git commit message style guidance missing from Conventional Commits 1.0.0

This is derived in part from the [Angular Commit Message
Format](https://github.com/angular/angular/blob/main/CONTRIBUTING.md#commit)
specification. ([`4ba18d6`](https://github.com/irtnog/lethbridge/commit/4ba18d6a0386df408fd4119a0b63c5594f900c58))

* docs: explain how to use the new Alembic wrapper and migration test fixture generator ([`705c2a2`](https://github.com/irtnog/lethbridge/commit/705c2a22b60a9c413e02936e48d1e28d35738bab))

### Fix

* fix(migrations): make ThargoidWar fields optional ([`fa5d008`](https://github.com/irtnog/lethbridge/commit/fa5d008f498b2653ae22af27c87a268a1d882c29))

* fix(migrations): switch to batch migrations

This is required if we want to continue supporting SQLite, which
imposes severe limits on `ALTER` statements.  See also [Running
“Batch” Migrations for SQLite and Other
Databases](https://alembic.sqlalchemy.org/en/latest/batch.html). ([`98ebf49`](https://github.com/irtnog/lethbridge/commit/98ebf4943c3f0218a898eb9bd487d3c184cd3448))

* fix(cli): disable Rich

This works around bugs in Typer or Rich, e.g., tiangolo/typer#578,
tiangolo/typer#622, and tiangolo/typer#646. ([`023aa33`](https://github.com/irtnog/lethbridge/commit/023aa332002c749e1adc6be49043501d29475577))

### Refactor

* refactor(migrations): shorten revision script names ([`6a75da3`](https://github.com/irtnog/lethbridge/commit/6a75da39b0e44401150bc59af4b143aea8197ac1))

### Test

* test(cli): check database migrations against mock galaxy data ([`42943a6`](https://github.com/irtnog/lethbridge/commit/42943a6c51b1a5d6461429d06c8ada6c13dfa1fb))

* test(cli): use the mock galaxy data in Spansh import integration testing

This is the first place where the data model and deserialization
schemas are checked against the Alembic-managed database schema as
opposed to the SQLAlchemy ORM version. ([`fb3a806`](https://github.com/irtnog/lethbridge/commit/fb3a806cf587b81def5a31da6050a666464d7a39))

* test(database): verify that null Thargoid War states work with the built-in schema ([`12bd1e6`](https://github.com/irtnog/lethbridge/commit/12bd1e6fdd061b162ab739e4ac2c06ff4033c0ea))

* test(database): add type hints to enable IDE tab completion ([`42d7f27`](https://github.com/irtnog/lethbridge/commit/42d7f276f722450fc5eaf2da9afa4af2e1558963))


## v0.2.1 (2023-12-03)

### Build

* build: replace aliases in target dependency lists with the actual artifacts in question

Otherwise, make will re-run targets unnecessarily. ([`656ccfd`](https://github.com/irtnog/lethbridge/commit/656ccfd3283ef5f047781d47ddb9573d7871f030))

* build: add alias for venv creation ([`5a91cf2`](https://github.com/irtnog/lethbridge/commit/5a91cf21ddaa6ff00c2c298df8c083395df5b691))

* build: sort imports before saving in Emacs ([`7ebf49a`](https://github.com/irtnog/lethbridge/commit/7ebf49a4763137216a5f3e220a56dc96991002a4))

* build(packaging): force Twine to parse the project README as Markdown, not reStructuredText

All the documentation says the content type gets detected
automatically, yet `twine check` as of Twine 4.0.2 fails with the
error &#34;\`long_description\` has syntax errors in markup and would not
be rendered on PyPI&#34;. ([`e016186`](https://github.com/irtnog/lethbridge/commit/e01618617d8c2e27ad5468cbc5d02ed88bae65b5))

### Ci

* ci: grant python-semantic-release permission to update the GitHub repo ([`00e99bd`](https://github.com/irtnog/lethbridge/commit/00e99bdd9094056847d12ce1f02772cdd7d9b335))

* ci: adjust publishing order to do TestPyPI before PyPI ([`2140c03`](https://github.com/irtnog/lethbridge/commit/2140c03660994ae83faca7816f2224cce276c08c))

* ci: limit test coverage reporting to this package ([`b60692b`](https://github.com/irtnog/lethbridge/commit/b60692b0426ffe98022762a97c16fd8a09982223))

* ci: cache the pytest report log instead of an empty file ([`ef8c160`](https://github.com/irtnog/lethbridge/commit/ef8c160a964224f46122f48996e9bd0bd4601dd2))

* ci: calculate the source hash based on file contents only

The previous version mistakenly included file system metadata in the
hash calculation. ([`6346270`](https://github.com/irtnog/lethbridge/commit/6346270c017b72b23f2821588bc7b52691865ef0))

* ci: reduce workflow execution time by caching dependencies, the working directory, and test results ([`60c1c6c`](https://github.com/irtnog/lethbridge/commit/60c1c6cf561eb5b820578aa9d82eaab20b91671a))

* ci: publish packages to PyPI and GitHub Releases ([`9136a28`](https://github.com/irtnog/lethbridge/commit/9136a28a36d86b35a91a5a4f49c6a75afcf45a3c))

* ci(release): publish package distributions to TestPyPI ([`93f50f4`](https://github.com/irtnog/lethbridge/commit/93f50f42d8ee9f0fab5b2a28bda3c3eb7c24bbb1))

* ci(release): cache the release and build jobs&#39; outputs ([`00f4b3e`](https://github.com/irtnog/lethbridge/commit/00f4b3e39cd492c81c15ad1cc24544873027d4be))

* ci(release): build distributions in an isolated, unprivileged environment

This stops privilege escalation attacks that work by injecting
malicious scripts into the build environment. ([`9320a3b`](https://github.com/irtnog/lethbridge/commit/9320a3b4c7639a0ec6c14cd0cdab02e1088737ca))

### Documentation

* docs: generalize some of the language used in the developer guidance ([`3c9b71b`](https://github.com/irtnog/lethbridge/commit/3c9b71b77ef04d47aadcc2b9caa2b0521c6b5c76))

* docs: add a build status shield ([`c4ae6e2`](https://github.com/irtnog/lethbridge/commit/c4ae6e27e3c0ff235e6bd0dbdd314b335af36947))

* docs: move developer guidance to a separate document ([`d1dc86e`](https://github.com/irtnog/lethbridge/commit/d1dc86e830f7fd6c293de5dc17fd68d9f91cca85))

* docs: remove preliminary content from the project&#39;s long description ([`25b5b04`](https://github.com/irtnog/lethbridge/commit/25b5b04018c5fdf52f4465e47cc82366da909148))

### Fix

* fix(lethbridge): migrate from pkg_resources to importlib.metadata

Cf. https://setuptools.pypa.io/en/latest/pkg_resources.html. ([`df6932e`](https://github.com/irtnog/lethbridge/commit/df6932ec7c6e3bd536293edb48b8fb1bcb7fc61c))


## v0.2.0 (2023-11-28)

### Build

* build(dev-infra): avoid removing packages other than the ones installed here ([`cfcf0ae`](https://github.com/irtnog/lethbridge/commit/cfcf0ae53a79025eb0aaf57fead4e53069abee29))

* build(dev-infra): add pre-commit targets plus some convenience aliases ([`7b4b09d`](https://github.com/irtnog/lethbridge/commit/7b4b09d3a4aa8fc60b8e996873e4170c35ce168d))

* build(dev-infra): update pre-commit hooks ([`178c7e6`](https://github.com/irtnog/lethbridge/commit/178c7e62dc0623b23eb13590b77320ee4cd96895))

* build(packaging): install pre-commit in the dev environment ([`8cc0cd2`](https://github.com/irtnog/lethbridge/commit/8cc0cd2a94bd0070fc0542ab089bd32f4b036213))

* build(dev-infra): add a quick smoke test target ([`e505b2b`](https://github.com/irtnog/lethbridge/commit/e505b2b0b9d09f0dff7d6a67ad87ba28b2aea0f1))

* build(packaging): add elpy RPC dependencies to the dev environment ([`cd8512b`](https://github.com/irtnog/lethbridge/commit/cd8512be8996142daf45a00022793e02d37e3182))

* build(dev-infra): add build dependency installation/removal targets ([`368e7a9`](https://github.com/irtnog/lethbridge/commit/368e7a93f044157cc31669e427dfc5f137a151fa))

* build(dev-infra): launch databases for developing Alembic migrations ([`14754e1`](https://github.com/irtnog/lethbridge/commit/14754e1f1191874a0c00a915dc256d4b85fa5f20))

* build(dev-infra): add targets for intermediate container stages, Docker cleanup ([`a36ea7f`](https://github.com/irtnog/lethbridge/commit/a36ea7fb1764dff8daa03079dcbbf73088d26ccc))

* build(dev-infra): simplify Python version check ([`a9ad65d`](https://github.com/irtnog/lethbridge/commit/a9ad65d85fa16329409d0d6dd15656cfa7cdb58b))

* build(dev-infra): consolidate make target aliases into one rule ([`e11b9c8`](https://github.com/irtnog/lethbridge/commit/e11b9c8713a6ae48320a49f60514b9937b25c162))

* build(dev-infra): work around outdated versions of pip, setuptools on older operating systems ([`0ae30ba`](https://github.com/irtnog/lethbridge/commit/0ae30bacbfe950a6a59e6ce6bd2aa7f8b404aff0))

* build(dev-infra): detect the active Python version

This affects some of the target pathnames. ([`77e18e4`](https://github.com/irtnog/lethbridge/commit/77e18e472594bad3fd2544478bae1cbec692da8f))

* build(dev-infra): install psycopg2cffi in the local dev environment

This matches the Docker container image build process. ([`4cc5ef8`](https://github.com/irtnog/lethbridge/commit/4cc5ef8eb1b0a3586e7b6370b04472ddc6e84cc0))

* build(dev-infra): define some useful shortcuts using make ([`faa7f4b`](https://github.com/irtnog/lethbridge/commit/faa7f4bc784d6955b0ac085e849c6af0a3090493))

* build: rename action to better reflect its purpose ([`848ce7a`](https://github.com/irtnog/lethbridge/commit/848ce7a793bb737f7a3306944d2c50445b7bf149))

### Ci

* ci(release): adopt semantic versioning and automate releases ([`ea38049`](https://github.com/irtnog/lethbridge/commit/ea380492adc74a9ec44ba42d4baae7625a4cdc1b))

* ci(test): validate the code against supported Python versions after linting ([`2a9be11`](https://github.com/irtnog/lethbridge/commit/2a9be117736b54ba05b413fe5d3621dd497f2dd1))

* ci(lint): simplify further by reusing the pre-commit hook ([`3ea9bdc`](https://github.com/irtnog/lethbridge/commit/3ea9bdc4a5fd6bf67643acb62b1d039e60c31514))

* ci(lint): simplify code style checks by relying on runner defaults ([`3efe833`](https://github.com/irtnog/lethbridge/commit/3efe833e1e7c365b690085cb62849ce33940903d))

* ci(lint): document workflow triggers ([`d54a8a0`](https://github.com/irtnog/lethbridge/commit/d54a8a0629102714e53b7a0d13d9dd5d100505e0))

### Documentation

* docs(schemas): explain why &#34;Object of type... not in session&#34; can be ignored ([`4254226`](https://github.com/irtnog/lethbridge/commit/4254226dad179d3327139bc11034066ffdc88a88))

* docs(schemas): explain the purpose of the stack in the Spansh schema test code ([`c6a6134`](https://github.com/irtnog/lethbridge/commit/c6a6134856ad7ef6349f30022746fb35e97945a0))

* docs(dev-infra): re-arrange comments and add vertical whitespace to improve section separation ([`f171ede`](https://github.com/irtnog/lethbridge/commit/f171edeca3d22799654045735ac2692fed229657))

* docs(packaging): add reference to PyPI classifiers list ([`d231ff6`](https://github.com/irtnog/lethbridge/commit/d231ff623193f922139f2875a67d26f872e15171))

* docs(dev-infra): explain what each set of make targets does ([`6246e4a`](https://github.com/irtnog/lethbridge/commit/6246e4abd4c8027f5e347a974c240de33362dc29))

* docs(docker): explain how the multi-stage build works to newcomers ([`ccce08f`](https://github.com/irtnog/lethbridge/commit/ccce08f672f6d50810ec1d1bf6686b9fd7d6a550))

* docs(docker): unhide example environment variables ([`3369da8`](https://github.com/irtnog/lethbridge/commit/3369da89ff23711acf3fa75947107eea4091ccf9))

* docs: add how to back up Docker volumes to the lessons learned ([`e477cff`](https://github.com/irtnog/lethbridge/commit/e477cff3f87455cdda31dfb748fb989a57cf62ea))

### Feature

* feat(packaging): bump to pre-alpha phase ([`7e0ec7d`](https://github.com/irtnog/lethbridge/commit/7e0ec7df13fc11d3284684a856fa1fd98b27c281))

* feat(docker): check the first argument for a subcommand and act accordingly ([`320fc90`](https://github.com/irtnog/lethbridge/commit/320fc908067539ed760ad8b4e0fbd9bf839f092e))

* feat(docker): parameterize the version of Python used in the container image ([`415a070`](https://github.com/irtnog/lethbridge/commit/415a0703c0f08722bea793ff906c715ed01fb0c9))

* feat(docker): initialize or update the database at container start ([`f6de7f2`](https://github.com/irtnog/lethbridge/commit/f6de7f2922c68e05713a00981a9cd19132f73d64))

* feat(cli): implement foreground imports of Spansh data dumps ([`1de48e5`](https://github.com/irtnog/lethbridge/commit/1de48e57481495418f3864b26c94fca7be5a826e))

* feat(migrations): use Alembic to manage database schema changes ([`bf48ba8`](https://github.com/irtnog/lethbridge/commit/bf48ba8cf86981c5451ce141e5270aff6cfb9061))

### Fix

* fix: remove unused imports ([`266aeb4`](https://github.com/irtnog/lethbridge/commit/266aeb47591bfbfa8079f0e9abfdc88bdcce0b5c))

* fix(database): prevent updates of all other classes using outdated data ([`37a4ef5`](https://github.com/irtnog/lethbridge/commit/37a4ef58d8c7f7a3d26141ac14de7cafcb706239))

* fix(database): prevent updates to a system from using outdated data ([`8b24f34`](https://github.com/irtnog/lethbridge/commit/8b24f34bba56ccd0fd98096b3baf2bdb76131423))

* fix(dev-infra): remove virtual env dependencies on system packages

This addresses issues with outdated packages conflicting with project
dependencies. ([`ab366e2`](https://github.com/irtnog/lethbridge/commit/ab366e224a1137884a8c5a485a1f24198a539c62))

* fix(docker): exclude Python bytecode from the container image

This improves Docker build cache management by excluding what are in
effect temporary files from the build context. ([`e706f73`](https://github.com/irtnog/lethbridge/commit/e706f7343c88c884670acceb7b60a5df826c5f0e))

* fix(docker): pass Lethbridge options specified in the container command to setup commands ([`5adcad7`](https://github.com/irtnog/lethbridge/commit/5adcad73ed3a75a268bd713c5a1b763fb6bfd03e))

* fix(cli): apply CLI logging level options to each configured logger ([`5ec4365`](https://github.com/irtnog/lethbridge/commit/5ec4365afaf35b705d8a0f42f2dc9c8b59f9f720))

* fix(database): make all Thargoid war state fields optional ([`b39ea43`](https://github.com/irtnog/lethbridge/commit/b39ea4301c49e36835c648f7815e531236682fdc))

* fix(docker): propagate the default database URI to the corresponding container environment variable ([`c1d8171`](https://github.com/irtnog/lethbridge/commit/c1d8171333e93b6cbd9552a33d0b748f40d37b94))

* fix(__main__): remove references to psycopg2cffi

This should be user-controlled. ([`281ac82`](https://github.com/irtnog/lethbridge/commit/281ac8250344032c2350d1c011e5257a0abb97b3))

* fix(cli): configure the actual root logger, not the application root ([`0a11704`](https://github.com/irtnog/lethbridge/commit/0a11704f16f49759727aff3d0d6f6d5f7eb8420d))

### Refactor

* refactor: sort imports ([`73597b0`](https://github.com/irtnog/lethbridge/commit/73597b04dfa32243b6eef1cba779930e7aa53048))

* refactor(packaging): re-sort sections alphabetically ([`08e5ac2`](https://github.com/irtnog/lethbridge/commit/08e5ac2d777876904fb444603f4c13a9dbb6257e))

* refactor(database): generalize validation function and move to base class

We can re-use the same code with different decorations in sibling
classes without having to copy/paste. ([`cb51380`](https://github.com/irtnog/lethbridge/commit/cb5138070e6a8ade71a1c54fd9a1c755da331a07))

* refactor(docker): drop planned support for MySQL/MariaDB

Getting [pytest-mysql](https://github.com/ClearcodeHQ/pytest-mysql) to
work has proven too difficult at this time. ([`d7d441a`](https://github.com/irtnog/lethbridge/commit/d7d441a18c174a4937dedb593f3a324b79bdcc7b))

* refactor(database): remove unused imports ([`cb5fe6a`](https://github.com/irtnog/lethbridge/commit/cb5fe6a28a49059cc2ca6c54cf683b600480c390))

* refactor(cli): break apart long string contants ([`344e6e1`](https://github.com/irtnog/lethbridge/commit/344e6e1f54542f10d03a6a3b372e9ae1a31bbc80))

* refactor(cli): simplify submodule loading ([`bae4188`](https://github.com/irtnog/lethbridge/commit/bae4188a05b809838ff36076635d32809b81be10))

* refactor(docker): optimize the build with better cache management ([`9869a96`](https://github.com/irtnog/lethbridge/commit/9869a96a493a4c0e7dd3c5bc2d6d0066938fcba0))

* refactor(docker): switch to composite Compose files

This enables overriding configuration items like port mappings:

https://stackoverflow.com/questions/48851190/docker-compose-override-a-ports-property-instead-of-merging-it

https://mindbyte.nl/2018/04/04/overwrite-ports-in-docker-compose.html ([`c51727e`](https://github.com/irtnog/lethbridge/commit/c51727e31db84b44c4dfaffa6ade026b82d0784f))

* refactor(docker): re-arrange layers in the build environment to cleanly separate test resources ([`72ea6a2`](https://github.com/irtnog/lethbridge/commit/72ea6a25454389ccfb0d2d832755e3d4f395ace5))

* refactor(cli): switch to a declarative logging configuration ([`9522726`](https://github.com/irtnog/lethbridge/commit/9522726be9d424dcbf18839a9021c00d76ad9dc3))

### Test

* test(cli): add more data to the Spansh import integration test ([`19a1209`](https://github.com/irtnog/lethbridge/commit/19a1209444310e445db8c357f87e18688da3cb2c))

* test(schema): add a smaller galaxy data fixture to speed up Spansh schema testing ([`f9d6ee2`](https://github.com/irtnog/lethbridge/commit/f9d6ee2429554f054c3ceb3aa93d6ad9dc7f153e))

* test(schema): make sure the System actually deserialized properly when getting and dumping it ([`3ede652`](https://github.com/irtnog/lethbridge/commit/3ede65263c876e7b54ed5e525b5ea2021715015b))

* test(schemas): suppress approximate match warnings ([`0913087`](https://github.com/irtnog/lethbridge/commit/09130876e37e9fa0cc74bf26ec46a07e7071912d))

* test: run CLI tests last since they&#39;re more properly integration tests ([`2979650`](https://github.com/irtnog/lethbridge/commit/29796506e40e6daa6fe327aa962b77febc8c78f6))

* test(database): capture &#34;approximately equal&#34; warnings ([`9286334`](https://github.com/irtnog/lethbridge/commit/92863349795bcf9e8ed3a67a393a6ba8b35bd03d))

* test(database): check the station outfitting model ([`6a02351`](https://github.com/irtnog/lethbridge/commit/6a023519a83b4728f9e7cefa57ffe4ba4e65e261))

* test(database): simplify the test station ([`c296485`](https://github.com/irtnog/lethbridge/commit/c296485aa22414ca15e21223cfbda89c65bdd420))

* test(database): check the station model ([`cffec43`](https://github.com/irtnog/lethbridge/commit/cffec43689493ed63c24376d5744f577f82ee990))

* test(cli): inline function args ([`f27e947`](https://github.com/irtnog/lethbridge/commit/f27e9473cd5fa8982fee9b90b51c089c8f4a46ae))

* test: mark slow tests so they can be skipped if desired ([`a8274d9`](https://github.com/irtnog/lethbridge/commit/a8274d9b533d4b5366049c2afa9931ac6236f51d))

* test: only generate the fixture corresponding to the mock_db_uri param

Previously, this was generating both
[postgresql](https://pypi.org/project/pytest-postgresql/) and
[tmp_path](https://docs.pytest.org/en/7.1.x/how-to/tmp_path.html) for
both fixture params, when really we wanted one or the other. ([`dbc4f36`](https://github.com/irtnog/lethbridge/commit/dbc4f36f86c2b732546db76f4f4690d76fd4f582))

* test: reconfigure smoke tests to use SQLite ([`3ad2637`](https://github.com/irtnog/lethbridge/commit/3ad263705159763c0e5de5e0f036b9853101a126))

* test: run cli tests after config, database tests but before schema tests

The cli tests exercise config, database, and schema functionality, but
since their test parameters are simpler, they function like smoke
tests for the much more complex schema tests. ([`8e65569`](https://github.com/irtnog/lethbridge/commit/8e65569500bf2f98a4593d633b404ba128fe15f8))

* test(cli): verify that Spansh imports work properly ([`a53463f`](https://github.com/irtnog/lethbridge/commit/a53463fe7de882812c1c8299dbc3e13f90480a3e))

* test(cli): verify that database schema migrations work properly ([`480a80c`](https://github.com/irtnog/lethbridge/commit/480a80cfa210723941abfa9084d160c14f450e0a))

* test: make mock_config_file available for integration tests ([`7de80f0`](https://github.com/irtnog/lethbridge/commit/7de80f0d3cc80fbeb632d1c256b0e9d5e186872d))

* test: increase the scope of the mock galaxy data fixture ([`65d263e`](https://github.com/irtnog/lethbridge/commit/65d263e777f0e67e7311c1e3301ab47416d600aa))

* test: convert mock galaxy data back into Spansh format for future integration testing ([`ad7a6f3`](https://github.com/irtnog/lethbridge/commit/ad7a6f3ea6364ef6b4e413d133f2f3a3d89a111f))

* test: switch to new mock database session with the schema already applied ([`49ca0f0`](https://github.com/irtnog/lethbridge/commit/49ca0f0d372de184d728764b5ea24a7e95d0bd74))

* test(cli): move configuration CLI tests to separate file ([`1dce5ec`](https://github.com/irtnog/lethbridge/commit/1dce5ecb805831cbfc57756815e2e46eac223abd))

* test: add Thargoid stronghold system to test data ([`2132e5e`](https://github.com/irtnog/lethbridge/commit/2132e5e5469958f197674082539662431d531e0b))


## v0.1.2 (2023-07-30)

### Build

* build: update flake8 configuration settings per Black&#39;s integration docs ([`9b5b22d`](https://github.com/irtnog/lethbridge/commit/9b5b22d6aeef6a444f74e2ed3e27824fc447b684))

### Documentation

* docs: record lessons learned ([`bb7354c`](https://github.com/irtnog/lethbridge/commit/bb7354c67504cae158be7a0eaea54987d7f60940))

* docs: outline deployment and development processes ([`51574b9`](https://github.com/irtnog/lethbridge/commit/51574b977f647235ada8c69ab57f74bb2dee9a70))

### Feature

* feat(database): model the state of the Second Thargoid War ([`edb43d1`](https://github.com/irtnog/lethbridge/commit/edb43d1952d5eea6f7e1ef9b7f76160831de2101))

* feat(docker): begin defining a deployment using Docker Compose ([`efecac8`](https://github.com/irtnog/lethbridge/commit/efecac80ce35235a192c412235548cb45ab887c5))

* feat(cli): add support for custom run-time initialization

Separate from configuration, this allows users to run arbitrary Python
code as part of the Lethbridge CLI start up process, e.g., to load
[psycopg2cffi](https://github.com/chtd/psycopg2cffi) in place of
psycopg2. ([`0815af9`](https://github.com/irtnog/lethbridge/commit/0815af9879740a07b16794c7b046830539699db0))

### Fix

* fix(cli): handle non-existent or defective init files ([`af51279`](https://github.com/irtnog/lethbridge/commit/af51279373afc5954f8c6884ca60710df6cb4a23))

* fix(packaging): pin to Python 3.10 or newer due to use of PEP 604 union types ([`6013582`](https://github.com/irtnog/lethbridge/commit/6013582202e68b464136c7f08c02eb2f19c95e4a))

* fix(schemas): replace deprecated class Meta option ([`d9829b6`](https://github.com/irtnog/lethbridge/commit/d9829b686f1e36a134ef278d2e95b6ef918004a5))

### Refactor

* refactor(docker): switch to a multi-stage build, with test resources excluded from the final image

While we&#39;re at it, pin to Python 3.10 to lower the risk of
compatibility issues. ([`a5d9f5d`](https://github.com/irtnog/lethbridge/commit/a5d9f5d1f136e1dfc6dfa5d3f670a44e3d596b21))

* refactor(packaging): move optional dependencies into their own section ([`1958120`](https://github.com/irtnog/lethbridge/commit/1958120e6e3eae3b2ec7329ae1b5316dad310393))

* refactor(packaging): remove unused dependency ([`6098f7a`](https://github.com/irtnog/lethbridge/commit/6098f7aac967f94c36cf9ccdc401ea1ce1defa82))

* refactor(docker): set PATH in image definitions ([`b00792c`](https://github.com/irtnog/lethbridge/commit/b00792c2441ea379a74ad4d7121201475a003402))

### Test

* test: accept decimals/floats within 5% of each other as being equal ([`917d10d`](https://github.com/irtnog/lethbridge/commit/917d10d98867626e921f11f4ccaae8f6aa747c1f))

* test: add approximate matches (with warnings) in certain cases ([`5eb3cfa`](https://github.com/irtnog/lethbridge/commit/5eb3cfa85dc3599fa67b554926ee9f84a833f2e8))

* test(schemas): re-enable flake8 errors

The marked variables are now intended to be used. ([`f854aa0`](https://github.com/irtnog/lethbridge/commit/f854aa0753c6d779ac3cf3ac540305944cc9b581))

* test: add Thargoid war system to test data ([`28a6b59`](https://github.com/irtnog/lethbridge/commit/28a6b595b618c5028b5a588066f522eb56bc28a9))

* test(schemas): rename test to match submodule ([`6246099`](https://github.com/irtnog/lethbridge/commit/6246099f3d34caf796eb6881ee5708f75a019114))

* test: rename galaxy data to match mock ([`8c1f8eb`](https://github.com/irtnog/lethbridge/commit/8c1f8ebbe41c5693e47fa26a6c5c091e9112f07a))

* test(cli): separate database CLI tests from the rest ([`9df0571`](https://github.com/irtnog/lethbridge/commit/9df05716e03da48710cb760c760bd5b0e342d61c))

### Unknown

* release: cut the v0.1.2 release ([`0ab70c2`](https://github.com/irtnog/lethbridge/commit/0ab70c20fb563e99456e75acd40ef96fd1e18be9))


## v0.1.1 (2023-07-25)

### Documentation

* docs(schemas): update note regarding system data processing order of operations ([`e2290df`](https://github.com/irtnog/lethbridge/commit/e2290dfb6a436068abe08063529eb49bdf326c7e))

* docs(schemas): remove extraneous comments/docstrings ([`cfe3f5b`](https://github.com/irtnog/lethbridge/commit/cfe3f5bc278c8c0e000be90101238c9b6ad87448))

### Feature

* feat(schemas): configure Marshmallow to use simplejson when parsing Spansh data dumps

Marshmallow needs this to properly support decimal.Decimal fields if
processing JSON data itself. ([`ab8dac5`](https://github.com/irtnog/lethbridge/commit/ab8dac5a4b6e2be45a14fa8e2da5cdda99901824))

* feat(database): include bodies in system comparisons ([`8d7f796`](https://github.com/irtnog/lethbridge/commit/8d7f796af610fe09078ae2ce343a24ab573f4dcf))

### Fix

* fix(database): re-order station columns to match class definition order ([`b081205`](https://github.com/irtnog/lethbridge/commit/b08120527659659fb070f19d14cbf605d0c137e3))

* fix(schemas): remove empty lists of signals from ring data dumps ([`d4bbc41`](https://github.com/irtnog/lethbridge/commit/d4bbc41a6ebc514d66503b2b43a68c26e604fec4))

* fix(schemas): remove empty lists of genuses, but this might not be correct in all cases ([`61c9e48`](https://github.com/irtnog/lethbridge/commit/61c9e48bd3e4d337949f2dfffb5bccd3e46c9f3a))

* fix(schemas): remove more table relationship fields from Spansh dumps ([`b277d18`](https://github.com/irtnog/lethbridge/commit/b277d18c708fdad881ef16fb13b90329afa56390))

* fix(schemas): convert 0.0 to 0 in Spansh dumps ([`da72525`](https://github.com/irtnog/lethbridge/commit/da72525333063edb3b4d5dee1bec302b419ff6d5))

* fix(schemas): keep empty station lists in Spansh dumps of body data ([`402c5d1`](https://github.com/irtnog/lethbridge/commit/402c5d1b4346608cd65a14fa5c82a07321218cec))

* fix(schemas): remove table relationship fields from Spansh dumps

These are implementation details, not body data. ([`55ca07b`](https://github.com/irtnog/lethbridge/commit/55ca07be97b545f951b818599335792885d5fbb2))

* fix(schemas): remove optional field from outfitting stock entry in Spansh dumps ([`3379276`](https://github.com/irtnog/lethbridge/commit/3379276ae8bd2b87fd73a87d112a12fdd71b4c2a))

* fix(database): use correct field name ([`1d9e3a3`](https://github.com/irtnog/lethbridge/commit/1d9e3a358831846c22c51e737419b5edd400f2d0))

* fix(schemas): check the context for the factions list explicitly

Otherwise, any other context data will cause faction context
initialization to be skipped. ([`19ade1f`](https://github.com/irtnog/lethbridge/commit/19ade1f99d78aaa0fdcd457bfd1fa10342e35754))

* fix(schemas): skip faction object memoization if the context isn&#39;t initialized ([`3a8c0b6`](https://github.com/irtnog/lethbridge/commit/3a8c0b6e7dc854f313c2c18fb8a4f0c6ecf5750f))

### Refactor

* refactor(database): switch from floats to decimals

The Python decimal.Decimal class preserves source precision better
than floats and is well supported by Marshmallow, SQLAlchemy, and
PostgreSQL.  Unfortunately, it isn&#39;t compatible with SQLite, so that&#39;s
potentially irreparably broken as of this commit. ([`44b629c`](https://github.com/irtnog/lethbridge/commit/44b629cf11a9ae87afc3f67f6ddc66e0678fe479))

* refactor(database): visually isolate foreign keys when practicable ([`b3beb0f`](https://github.com/irtnog/lethbridge/commit/b3beb0f86970eaef45c7f0b356d2ef29777842bc))

* refactor(schemas): de-serialize the station economies dictionary the same way as others ([`db35812`](https://github.com/irtnog/lethbridge/commit/db3581272d4e84d91dd1f4b96b0357961439095a))

* refactor(schemas): simplify faction state data pre/post-processing ([`6a0ecec`](https://github.com/irtnog/lethbridge/commit/6a0ecec0a75763119803f3b1950fcd382fa9c656))

* refactor(schemas): simplify outfitting stock data pre/post-processing ([`8bf9a0d`](https://github.com/irtnog/lethbridge/commit/8bf9a0d4ccd464620af2d8acf3a1ef50e4f07e39))

* refactor(schemas): simplify station data pre/post-processing ([`76b442f`](https://github.com/irtnog/lethbridge/commit/76b442fa24b4fb0e677de4f23f0e0c40ada44986))

* refactor(schemas): simplify body data pre/post-processing ([`ebe4217`](https://github.com/irtnog/lethbridge/commit/ebe42170ac03c9ff797b5e4a580a993d7421f697))

* refactor(schemas): simplify system coordinate data pre/post-processing ([`82e88d7`](https://github.com/irtnog/lethbridge/commit/82e88d74db85566ea4e5bbd0096768e3b28a6740))

* refactor(schemas): move the Spansh schema to its own module ([`747347f`](https://github.com/irtnog/lethbridge/commit/747347f18c868adfb9717d6cde64d899fde317bc))

### Test

* test: reconfigure smoke tests to use PostgreSQL ([`5a531f7`](https://github.com/irtnog/lethbridge/commit/5a531f7fed5ae4d15202306c83bb482528c83723))

* test(schemas): perform a depth-first comparison of the source data and database contents ([`4dd5791`](https://github.com/irtnog/lethbridge/commit/4dd5791064b8071482da8bb0d2686bb3382aaee0))

* test: rename mock galaxy data to better reflect its purpose ([`df955c1`](https://github.com/irtnog/lethbridge/commit/df955c13550726de89276df25147cf2fc04a9b24))

### Unknown

* release: cut the v0.1.1 release ([`d72e534`](https://github.com/irtnog/lethbridge/commit/d72e534b3adcfaa3b660daed79bc9ede17255e7a))


## v0.1.0 (2023-07-23)

### Feature

* feat(database): model a body&#39;s volcanism type and reserve level

And with this commit, all of the test data appears to load correctly! ([`cf70541`](https://github.com/irtnog/lethbridge/commit/cf70541eb6969c64ee34b97190d2e2f0735d40cf))

* feat(database): model a solid body&#39;s raw material abundance ([`b68384a`](https://github.com/irtnog/lethbridge/commit/b68384a1949804730ae3760396fe686458f38893))

* feat(database): model belts and rings ([`8b7bc60`](https://github.com/irtnog/lethbridge/commit/8b7bc60987a73d2993e4aad09e3aeabf105fc4b7))

* feat(database): model a body&#39;s parent bodies ([`43f804a`](https://github.com/irtnog/lethbridge/commit/43f804ac89dfebbe35df5a97497788d6132a0d07))

### Unknown

* release: cut the v0.1.0 release ([`4f56b9a`](https://github.com/irtnog/lethbridge/commit/4f56b9a0095bd094e8ab680399c07881976eecc1))


## v0.0.9 (2023-07-19)

### Documentation

* docs(database): remove code tags for Anarchy/None and powerState

The string values `Anarchy` or `None` are distict from the None value
in that the latter means the datum in question wasn&#39;t available.

The powerState key probably denotes Bubble systems, but there isn&#39;t a
straightforward way to model this. ([`b217347`](https://github.com/irtnog/lethbridge/commit/b21734738654c93c177a84271c5ff6adedba47b8))

### Feature

* feat(database): model body scan timestamps ([`2ee0561`](https://github.com/irtnog/lethbridge/commit/2ee0561c344395d5295ec429779c262d5010ee4d))

* feat(database): model a body&#39;s detailed surface scan data ([`0d62b2e`](https://github.com/irtnog/lethbridge/commit/0d62b2e1378b3892f2375432522aeda312c89b1b))

* feat(database): model a body&#39;s solid composition ([`d81dec1`](https://github.com/irtnog/lethbridge/commit/d81dec148816d8309899f53c494e135a2b5d7b94))

### Refactor

* refactor(database): move body composition data pre-processing into the appropriate schemas ([`3ba24c9`](https://github.com/irtnog/lethbridge/commit/3ba24c9d31df78c529dc52cfadfb61a9d599feb6))

* refactor: initialize pyscopg2cffi at app load time

Library callers should not be forced to use this package. ([`293ef5b`](https://github.com/irtnog/lethbridge/commit/293ef5b8e419267a39ba102c4bb8c041b7723abc))

### Unknown

* release: cut the v0.0.9 release ([`d59359c`](https://github.com/irtnog/lethbridge/commit/d59359cf5423ba25fd92b13fd128486fb10a8e9c))


## v0.0.8 (2023-07-17)

### Documentation

* docs(database): answer question about station allegiance/government

Yes, that&#39;s supposed to match the controlling faction, but no, it
doesn&#39;t always. ([`f811b5f`](https://github.com/irtnog/lethbridge/commit/f811b5f53302e4f5b0377382da791dfbb7db1f40))

* docs(database): give body objects a description ([`0840d8a`](https://github.com/irtnog/lethbridge/commit/0840d8a3895acbc4795110adfb8765e7c7576750))

* docs(database): use similar language to the wiki when describing powers ([`e49ea28`](https://github.com/irtnog/lethbridge/commit/e49ea281f083a85b3bee764465cf1e81c426286d))

* docs(database): use similar language to the wiki when describing factions ([`2d70539`](https://github.com/irtnog/lethbridge/commit/2d70539c265934ec06c536c4a58c727ca469e684))

### Feature

* feat(database): model a body&#39;s atmospheric composition ([`eb08e8c`](https://github.com/irtnog/lethbridge/commit/eb08e8c7b1d5a929c4f0241e27e67a67ce261f21))

* feat(database): implement pretty printing and equivalence tests for various station services ([`bd369f7`](https://github.com/irtnog/lethbridge/commit/bd369f7ee2538e501434c2db626d072698d15772))

* feat(database): implement equivalence tests for bodies ([`6d8b2d8`](https://github.com/irtnog/lethbridge/commit/6d8b2d87528b66338311bbce57260bc4ffd502f7))

* feat(database): denote StationEconomy objects in an intermediate state ([`7398115`](https://github.com/irtnog/lethbridge/commit/739811525223caf2be1a20b9eda9edffd6303712))

* feat(database): pretty print Body ([`6f71195`](https://github.com/irtnog/lethbridge/commit/6f71195335138c8b99daa6119ea5ae5322fb72b7))

* feat(database): throw an error on unknown system fields ([`341f332`](https://github.com/irtnog/lethbridge/commit/341f33238426a172cdd9eb0f766e6dfd4abfd733))

* feat(database): model bodies ([`2815c3d`](https://github.com/irtnog/lethbridge/commit/2815c3d0b47fce74f049b4c2b1dd335ad6aafec1))

### Fix

* fix(database): include the station update time in its equivalence check ([`45d7583`](https://github.com/irtnog/lethbridge/commit/45d7583f0c6d967e509f5b786da3042fae41e4e2))

* fix(database): ignore a commodity&#39;s translated name or commodity ID ([`1603827`](https://github.com/irtnog/lethbridge/commit/16038273848b800cce2e60536214ca70f91b85a8))

* fix(database): work around bad market data by treating all order columns as primary keys ([`1b7e15d`](https://github.com/irtnog/lethbridge/commit/1b7e15d8500c0a64dc349cf80a56e6b9b522854c))

* fix(database): de-serialize a system&#39;s factions first

Sometimes, a station&#39;s data on a faction can be invalid or missing.
For example, Pettitt Metalurgic Base on 36 Ophiuchi A 1 a in the test
galaxy data claims the 36 Ophiuchi Autocracy faction is
Federation-aligned due to these journal entries:

https://edgalaxydata.space/eddn-lookup/extract.php?filename=Journal.Docked-2022-09-19.jsonl.bz2&amp;lineno=7315

https://edgalaxydata.space/eddn-lookup/extract.php?filename=Journal.Docked-2023-01-01.jsonl.bz2&amp;lineno=11071

While the Marshmallow documentation for the knob mentions
serialization, setting `ordered = True` and listing the schema fields
in this order appears to lead to the desired result---that the
system&#39;s factions get created (and memoized) from the system&#39;s
`factions` field first.  Then when Marshmallow processes the system&#39;s
stations and bodies, any faction references will use the cached
Faction object.

https://marshmallow.readthedocs.io/en/stable/marshmallow.schema.html#marshmallow.schema.Schema.Meta ([`f98a60f`](https://github.com/irtnog/lethbridge/commit/f98a60fa97437150da051ce441c498e77109d602))

### Refactor

* refactor(database): consolidate PowerPlay classes ([`bc8a015`](https://github.com/irtnog/lethbridge/commit/bc8a0154ff9c7da20fd16d053a2cab510c5cefb3))

* refactor(database): simplify the station&#39;s pretty printed representation ([`4c42b08`](https://github.com/irtnog/lethbridge/commit/4c42b0806dae3bb3547cd5ab7ae3f5b2409aed6f))

* refactor(database): order columns in the order of their corresponding class&#39;s/attribute&#39;s appearance ([`d32d706`](https://github.com/irtnog/lethbridge/commit/d32d706559efedd86d6051a071b662d8b1265c55))

* refactor(database): rename class to emphasize its connect to factions ([`fc3d254`](https://github.com/irtnog/lethbridge/commit/fc3d2540f4d7e9e8baea983d9e03b61c3390eff8))

* refactor(database): record a station&#39;s shipyard data in a dedicated Shipyard class ([`ba80e53`](https://github.com/irtnog/lethbridge/commit/ba80e5340703b264c136e10fcef80766f24d451e))

* refactor(database): record a station&#39;s outfitting data in a dedicated Outfitting class ([`ee8fc71`](https://github.com/irtnog/lethbridge/commit/ee8fc712bc99934fea6da5a0b75c07a351198f20))

* refactor(database): record a station&#39;s market data in a dedicated Market class

This should make future market data updates and date comparisons
simpler. ([`7eb3ae1`](https://github.com/irtnog/lethbridge/commit/7eb3ae12eb399123db88550460104c15e754afe6))

* refactor(database): don&#39;t waste time sorting the factions and powers lists

This ordering was only done to facilitate testing and is not needed
any more. ([`cc9e293`](https://github.com/irtnog/lethbridge/commit/cc9e2934a9010a2765bfa80160dee5421936107c))

* refactor(database): rename station attributes to better match Spansh ([`8f505df`](https://github.com/irtnog/lethbridge/commit/8f505dfbed078d89f50a9166641037477dd79351))

* refactor(database): rename ShipyardStock to match OutfittingStock ([`643bee1`](https://github.com/irtnog/lethbridge/commit/643bee13ca7ce40188d1c7abc882ce608c6437c4))

* refactor(database): memoize Faction objects using the Marshmallow context

This makes Faction de-duplication much simpler compared to walking the
System and nested/related objects. ([`2ed5103`](https://github.com/irtnog/lethbridge/commit/2ed5103ca509d81226941d9d8f1d5fc2aad485df))

### Test

* test(database): disable SQL statement echoing

Due to the volume of log data generated by this flag, it&#39;s no longer a
useful debugging aid. ([`eb70d9f`](https://github.com/irtnog/lethbridge/commit/eb70d9f72696e33445842b25041d9be5e0195af7))

### Unknown

* release: cut the v0.0.8 release ([`931b988`](https://github.com/irtnog/lethbridge/commit/931b9885bda7093a1703387ffdc0d76b11eead6b))


## v0.0.7 (2023-07-12)

### Feature

* feat(database): model station shipyards ([`6236fe6`](https://github.com/irtnog/lethbridge/commit/6236fe67082eb5bcae67b6dad7c4be893681d56e))

### Fix

* fix(docker): run the installation and testing processes from the source directory ([`b73b7b1`](https://github.com/irtnog/lethbridge/commit/b73b7b177d646b4d53620321cd9872291cdb3644))

### Test

* test(database): simplify attribute access ([`e166e36`](https://github.com/irtnog/lethbridge/commit/e166e36a539060308f5d8e8f738f6b272072869a))

### Unknown

* release: cut the v0.0.7 release ([`9f91a0d`](https://github.com/irtnog/lethbridge/commit/9f91a0dd52da835ddb88383ba783fdeedde90741))


## v0.0.6 (2023-07-12)

### Feature

* feat(database): model station outfitting ([`92842f5`](https://github.com/irtnog/lethbridge/commit/92842f5d610b8eb9d341148d4c39b6b770a05815))

### Refactor

* refactor(database): remove unneeded symbol prefixes ([`ab98fb5`](https://github.com/irtnog/lethbridge/commit/ab98fb5f26032e01d85da7cdc2beae2b83a06608))

* refactor(database): simplify PowerPlay (de-)serialization ([`43ea2a3`](https://github.com/irtnog/lethbridge/commit/43ea2a3348ade7192951846b2430c5d44c0ad63a))

* refactor(database): eliminate unnecessary copying ([`f1f9625`](https://github.com/irtnog/lethbridge/commit/f1f9625607ca8480658b26609ad79bf13b277bfa))

* refactor(database): simplify prohibited commodity de-serialization ([`ea2c8ec`](https://github.com/irtnog/lethbridge/commit/ea2c8ec69b4b24662e821ba99e8d5af25f6324a8))

* refactor(database): simplify station service (de-)serialization ([`3d554a5`](https://github.com/irtnog/lethbridge/commit/3d554a5e3eee7b8393de85002cf6407ca18de04e))

* refactor(database): simplify BGS state/faction de-serialization

More importantly, move preprocessing into the appropriate Marshmallow
schemas instead of SystemSchema. ([`e3958ce`](https://github.com/irtnog/lethbridge/commit/e3958cebb95205c47f882b4c26855cb049813a1a))

### Test

* test(database): revise and expand system data (de-)serialization checks ([`3abfc9a`](https://github.com/irtnog/lethbridge/commit/3abfc9a8638cbd7e54813674028038a1f26096e0))

* test(database): check date handling across all target databases ([`cb6b1fe`](https://github.com/irtnog/lethbridge/commit/cb6b1fe594346538e49cad1991de681f0fa8bdc1))

* test(database): consolidate tests and test data ([`059a446`](https://github.com/irtnog/lethbridge/commit/059a44663e72120bb7545df20146a1b809dd1ce9))

### Unknown

* release: cut the v0.0.6 release ([`23927be`](https://github.com/irtnog/lethbridge/commit/23927be6a395e26e78d2f0d2915e46c7db7b9bd3))


## v0.0.5 (2023-07-10)

### Build

* build: re-configure flake8 to match Black style ([`6c15489`](https://github.com/irtnog/lethbridge/commit/6c15489d5fd4ca3a1facdd68525d4b78baa4a40d))

* build: check code style at commit time ([`656c807`](https://github.com/irtnog/lethbridge/commit/656c8070ad935b98ddd38617c66afe91cb3e38c6))

* build: check code style on push/pull request ([`3fe5a52`](https://github.com/irtnog/lethbridge/commit/3fe5a5229595d608ce3a027fa988eef23e21d6c6))

### Documentation

* docs(database): remove extraneous whitespace from ORM class docstrings ([`f390b9f`](https://github.com/irtnog/lethbridge/commit/f390b9f065130a11c39b90d44377987eefd481e5))

### Feature

* feat(database): implement printed representations and equality checks for ancillary ORM classes ([`a187e71`](https://github.com/irtnog/lethbridge/commit/a187e719ac597357b0b527a44ded0410c41972b4))

* feat(database): model station markets ([`7551c81`](https://github.com/irtnog/lethbridge/commit/7551c81ab3a0821fa07f9f199dfc379adf685cdc))

* feat(database): model station economies ([`498c35c`](https://github.com/irtnog/lethbridge/commit/498c35c915648ee657fe38e2afb65f8167a9c6a6))

* feat(database): model station services ([`1ca7de7`](https://github.com/irtnog/lethbridge/commit/1ca7de7e9c0ded14f9d7a490444b171ad80726da))

* feat(database): model station landing pads ([`8142cf6`](https://github.com/irtnog/lethbridge/commit/8142cf6a792f5894218ea73aa88b6a043d5f3bcd))

### Refactor

* refactor(database): rename StationService&#39;s primary key to match other ORM classes ([`8e628b7`](https://github.com/irtnog/lethbridge/commit/8e628b71d69a4588e6b957b263fa8588b2c8c497))

* refactor(database): post-process station attributes in order of their appearance ([`fc3f7b7`](https://github.com/irtnog/lethbridge/commit/fc3f7b765847eaf258d989b8590b7e494bdc80a8))

* refactor(database): remove plural from table name ([`7acb3ee`](https://github.com/irtnog/lethbridge/commit/7acb3eee6e83e51b14113dab3bba8780688fbc09))

* refactor(database): simplify empty key cleanup processes ([`6ae0486`](https://github.com/irtnog/lethbridge/commit/6ae04869ca2b63f3801a161ee94426aae701f1f7))

### Unknown

* release: cut the v0.0.5 release ([`4b83491`](https://github.com/irtnog/lethbridge/commit/4b834916e364da07eff8cf5b09387ad0a275b50c))


## v0.0.4 (2023-07-08)

### Documentation

* docs(database): remove prompt about faction identifers

We&#39;ll stick with names.  It makes de-duplication and updating simpler. ([`531403c`](https://github.com/irtnog/lethbridge/commit/531403cf856f6160089cfe3d0f3f31cd69765e61))

* docs(database): move comments to doctrings, fix grammar, and tag questionable code ([`9a8dcc0`](https://github.com/irtnog/lethbridge/commit/9a8dcc006d2bba1d5654c147597154b79fa91337))

### Feature

* feat(database): model stations ([`5b87047`](https://github.com/irtnog/lethbridge/commit/5b87047b2c2552078ca9fe0b6b485112d427cca3))

* feat(database): simplify faction de-duplication at system de-serialization time ([`9b68aee`](https://github.com/irtnog/lethbridge/commit/9b68aeeb5e48a12ed15c6de1644694428a2f7475))

* feat(database): make faction allegiance and government optional

This is required by fleet carriers. ([`3b0d4dc`](https://github.com/irtnog/lethbridge/commit/3b0d4dc09e401bd088e07fe8b94de610d83958c6))

* feat(database): give PowerPlay objects a printed representation ([`223ca0e`](https://github.com/irtnog/lethbridge/commit/223ca0eaeef2705880f34c45b1eadf339012f03b))

* feat(database): implement missing System equality checks ([`53c34e7`](https://github.com/irtnog/lethbridge/commit/53c34e7d90c6fad5d76c87241cb43a821ecf178e))

### Fix

* fix(database): use the Faction object&#39;s representation when printing BGS states ([`19fb3f0`](https://github.com/irtnog/lethbridge/commit/19fb3f05c8e5ab39476f26419bb854b75c557611))

### Test

* test(database): restructure multiple conditional statements when comparing serialized systems ([`dc10415`](https://github.com/irtnog/lethbridge/commit/dc104152b607c943e635e3922cf5a3f45ca5727c))

* test(database): re-order operations to match attribute/column order ([`bbdf6a7`](https://github.com/irtnog/lethbridge/commit/bbdf6a7352af4ced811d903943a16ca5a635d72d))

* test(database): validate PowerPlay earlier in the ORM tests ([`f27f254`](https://github.com/irtnog/lethbridge/commit/f27f254d7e5400d40ca26eafd977cd2b763fb279))

* test: remove unnecessary tests and limit smoke testing to just SQLite ([`3dcfb6c`](https://github.com/irtnog/lethbridge/commit/3dcfb6cd48a8bfb0dfb5b70261ca23fdd2b74088))

* test: wrap long lines in database mockup ([`81c52d8`](https://github.com/irtnog/lethbridge/commit/81c52d83ee8b3ad332a444e90296bd9c2d9466df))

### Unknown

* release: cut the v0.0.4 release ([`dc83556`](https://github.com/irtnog/lethbridge/commit/dc8355657221db46662800559d52379ffad0372d))


## v0.0.3 (2023-07-06)

### Documentation

* docs(database): correct a grammatical error ([`587468e`](https://github.com/irtnog/lethbridge/commit/587468e5fc5a6ccf21d0fea547f1aa2114c14c5f))

### Feature

* feat(database): model PowerPlay ([`070b223`](https://github.com/irtnog/lethbridge/commit/070b22385d36a64ec2d7b84f7613ee308a8add68))

### Refactor

* refactor(database): simplify pre/post-dump/load processing ([`54bc2ce`](https://github.com/irtnog/lethbridge/commit/54bc2ceec52f3f7ff7b8182ce4045a732b93a847))

* refactor(database): list autoschema exclusions in their order of appearance in the model class ([`2d9702d`](https://github.com/irtnog/lethbridge/commit/2d9702db39fdeb306f53f3bd00d46ab2bc66162f))

### Test

* test(database): import multiple, related systems at once ([`62bbf54`](https://github.com/irtnog/lethbridge/commit/62bbf5474f4e276fbe62f1a70adb78d889b592c4))

### Unknown

* release: cut the v0.0.3 release ([`12d532c`](https://github.com/irtnog/lethbridge/commit/12d532c6c575185f50dfb5d2718d074fcf660d5b))


## v0.0.2 (2023-07-04)

### Documentation

* docs(database): remind readers that modifying dicts in loops results in an exception ([`3a247c8`](https://github.com/irtnog/lethbridge/commit/3a247c8032dd27339a18c5069f1d220ec229f950))

### Feature

* feat(database): (de-)serialize faction data, matching Spansh&#39;s galaxy data dump ([`6a2d8b3`](https://github.com/irtnog/lethbridge/commit/6a2d8b3c3c931e2c991486dd1cd73264292b4851))

* feat(database): pretty print BGS states ([`ecbecde`](https://github.com/irtnog/lethbridge/commit/ecbecdecdfc5e98338812378cb801f7b1fcf34f1))

* feat(database): switch to new-style (Python 3.10+, PEP 604) Union type syntax

This syntax doesn&#39;t work with indirect ORM class references, so leave
that one alone.

Also note that the existing `__future__` import should make this
syntax work on Python 3.7+. ([`9bac86f`](https://github.com/irtnog/lethbridge/commit/9bac86fa2f9140670a0f06f5dd8f2acc77404984))

* feat(database): define serialization schemas for factions and BGS states ([`69e64c9`](https://github.com/irtnog/lethbridge/commit/69e64c934b85d9523cd6fb5dae8aa786cec5ef84))

* feat(database): model factions and their BGS states ([`ea70baa`](https://github.com/irtnog/lethbridge/commit/ea70baa9260276706ced2c893209e786a277b13e))

### Fix

* fix(database): resize System.population as the default type mapping is too small on PostgreSQL ([`7d7634b`](https://github.com/irtnog/lethbridge/commit/7d7634b3756f95127fea50359110afc23bdf30f9))

* fix(database): sort serialized faction data, again to match Spansh ([`506cd28`](https://github.com/irtnog/lethbridge/commit/506cd28a9e831a97c023bf5b289cf181716cf617))

* fix(database): flatten faction data in BGS state dumps ([`6cb1438`](https://github.com/irtnog/lethbridge/commit/6cb14383cae278dc1d3e98c9f45050cfcc0694e9))

* fix(database): remove the ORM-managed faction name (foreign key) from BGS state dumps ([`b7b5447`](https://github.com/irtnog/lethbridge/commit/b7b54472232d5be193fad6729a8411aaff42ca5b))

* fix(database): avoid copying the output dict if not required ([`daf3693`](https://github.com/irtnog/lethbridge/commit/daf36930ed0d53aac0615e242ce25caa270c7c4c))

* fix(database): resize System.id64 as the default type mapping is too small on PostgreSQL ([`eb8f883`](https://github.com/irtnog/lethbridge/commit/eb8f8834a60a43c2dbac1d59a702b3692ef5b29c))

* fix(database): remove empty columns from the dump, matching Spansh ([`10cb937`](https://github.com/irtnog/lethbridge/commit/10cb9377f30a5c9a42d4824bfac4bfc8a9ef1711))

* fix(database): remove ORM relationship management columns from dumps ([`a2a0a6f`](https://github.com/irtnog/lethbridge/commit/a2a0a6faf7c80d8355a213017ae48d6a912ef4a1))

* fix(database): do not mutate inbound (pre-load) or outbound (post-dump) data structures

This violates the Principle of Least Astonishment.  Make copies for
yourself, instead. ([`8771db7`](https://github.com/irtnog/lethbridge/commit/8771db71d184230bd517b7e88b979e99226722da))

* fix(database): exclude foreign keys from system data dumps

Spansh represents relationships using nesting, even though it results
in duplicate copies of the relevant data (e.g., faction name,
allegiance, and government). ([`48c9d86`](https://github.com/irtnog/lethbridge/commit/48c9d860906fcf195def4ee62b85af3b05b38720))

* fix(database): model controlling factions as nullable many-to-one relationships ([`c4b0925`](https://github.com/irtnog/lethbridge/commit/c4b0925ad214cd2cc2c302ad014082004dc0d5b4))

* fix(database): make database re-initialization flag optional ([`b13535f`](https://github.com/irtnog/lethbridge/commit/b13535f3241575cc48a6902769cf0afa854fa25e))

### Refactor

* refactor: format Python code using Black ([`8bd018c`](https://github.com/irtnog/lethbridge/commit/8bd018c94eed4c6510763a5e58d4ccc8291d3fca))

* refactor(database): remove unused import ([`aa14c94`](https://github.com/irtnog/lethbridge/commit/aa14c94bb9a86a3e8aecbe524c489841443620ca))

### Test

* test(database): log SQL for troubleshooting purposes ([`280cea1`](https://github.com/irtnog/lethbridge/commit/280cea11317a69e0b2b33480a654c4e07b77ca3c))

* test(database): match input date/time format to Marshmallow&#39;s default output ([`92389bf`](https://github.com/irtnog/lethbridge/commit/92389bf89f7dfd9026417a2567d17c0f5c165896))

* test: narrow smoke tests to deserialization with fake data ([`b564de9`](https://github.com/irtnog/lethbridge/commit/b564de9ac7680725d7332c76441d0a8fa636d5be))

* test(database): add a smoke test for the System serialization schema ([`7772a55`](https://github.com/irtnog/lethbridge/commit/7772a5538907696c3ae8381f46c67108ac593ef1))

* test(database): rename index variable to better hint at purpose ([`cf7aeed`](https://github.com/irtnog/lethbridge/commit/cf7aeedc286d15a7d7b63ffb9588b4b7c9b7f1f1))

* test: define a set of preliminary tests, currently focused on the database ([`c4e4441`](https://github.com/irtnog/lethbridge/commit/c4e4441b69601eba89b977308a276a522e8b4981))

* test(database): remove unused fixture ([`0ddfd74`](https://github.com/irtnog/lethbridge/commit/0ddfd7446575af375a3984472d101bd64a513d27))

* test: reformat test data using jq for readability ([`baa7b36`](https://github.com/irtnog/lethbridge/commit/baa7b36bc739a1ba92c431913de2f2df9bf4e723))

* test(docker): report on test coverage during the build ([`ea4cc61`](https://github.com/irtnog/lethbridge/commit/ea4cc6145b45fbf82a546aa2a6f460b2e2842d07))

* test(database): skip system data timestamp checks for now ([`953b573`](https://github.com/irtnog/lethbridge/commit/953b573ffba67a9c1299ae54fcb308c0077d30c8))

* test(database): remove unused imports ([`8cb4b8f`](https://github.com/irtnog/lethbridge/commit/8cb4b8f009f004c625e9db6f4d92b10bfcff004e))

* test(database): remove redundant database schema checks

This gets checked by the CLI tests. ([`5d96096`](https://github.com/irtnog/lethbridge/commit/5d96096191287b9cbc6d043844b7b7d25f63565c))

* test(database): use real galaxy map data to test the serialization schema ([`d0902e3`](https://github.com/irtnog/lethbridge/commit/d0902e3d8e457cb3df39327872a675eb810eb60b))

* test(database): parameterize the database URI fixture ([`8160df2`](https://github.com/irtnog/lethbridge/commit/8160df2a85bc7d0eb35a30e797e3dc9665fca8f8))

* test(database): run relationship tests in a separate session/transaction ([`b6869d9`](https://github.com/irtnog/lethbridge/commit/b6869d9cd5480b3309bae09e722769f40eb093b9))

* test(database): verify system/faction/BGS state associations ([`7b56cee`](https://github.com/irtnog/lethbridge/commit/7b56ceea3316a8f1fa7de7b1de9a4bad03256e16))

* test(database): verify integrity constraints and query results ([`43ad80c`](https://github.com/irtnog/lethbridge/commit/43ad80c967dd72cb99ad01e3826075abb3340807))

* test(database): simplify the ORM test ([`132e8e1`](https://github.com/irtnog/lethbridge/commit/132e8e12a288e271f91ab398ede2e8e1c9318b9c))

### Unknown

* release: cut the v0.0.2 release ([`8dab70a`](https://github.com/irtnog/lethbridge/commit/8dab70a638b802bbeb57a939e8338df2a399f359))


## v0.0.1 (2023-06-29)

### Documentation

* docs(packaging): add license metadata ([`728ba8e`](https://github.com/irtnog/lethbridge/commit/728ba8eadcad7171d61180b1b6d838f8c54416a9))

* docs: correct EDDN name and link ([`19ad4e2`](https://github.com/irtnog/lethbridge/commit/19ad4e20f62866d8bad58b69121160a1b2d78cf6))

### Feature

* feat: implement configuration editing via the CLI

This requires modifying a lot of stuff to replace global variables
with the
[Typer context](https://typer.tiangolo.com/tutorial/commands/context/). ([`2b9ab56`](https://github.com/irtnog/lethbridge/commit/2b9ab564d9862c94dab110b2eb8f9166964e88cd))

* feat(config): load config files into the specified ConfigParser object

This makes it possible to save just modified configuration settings. ([`2706eda`](https://github.com/irtnog/lethbridge/commit/2706eda8589f9fb9a2e47d66fec5a896012a3997))

* feat(cli): mock up the rest of the CLI ([`10d1579`](https://github.com/irtnog/lethbridge/commit/10d1579e38a2eb7f253f42a9892581d246b54e39))

* feat(cli): keep track of the overridden configuration file name

That way, the `configure` subcommand knows in which file to save
configuration changes. ([`be2d13c`](https://github.com/irtnog/lethbridge/commit/be2d13cbbb640dcc57241592730f973cd3230354))

* feat(config): move the default SQLite database to the current working directory

Whether the configuration directory exists depends on whether a
configuration setting has been changed. ([`010da9c`](https://github.com/irtnog/lethbridge/commit/010da9c72bd0e5ee4d585aede3da0139d8eac6e0))

* feat(database): add database initialization function ([`ae8f92d`](https://github.com/irtnog/lethbridge/commit/ae8f92d9cfb6373325e86e3f0e09ea55bbf98571))

* feat(cli): load the configuration file at CLI start time

This lets other tools use Lethbridge as a library and control things
like configuration themselves. ([`98aa196`](https://github.com/irtnog/lethbridge/commit/98aa19662aa7d478f84c72d27eb452da4d61fd58))

* feat(cli): show help for subcommands ([`554bc6a`](https://github.com/irtnog/lethbridge/commit/554bc6ad0733dc67d8eb00b82857207090122071))

* feat(config): simplify to a thin wrapper around configparser ([`e8952d0`](https://github.com/irtnog/lethbridge/commit/e8952d0354f04ca81025c11296f46428ec274958))

* feat(cli): automatically load subcommands from submodules ([`b66a7ea`](https://github.com/irtnog/lethbridge/commit/b66a7ea6f03550aa63b3fb6ee07d17b842855c49))

* feat(cli): allow overriding the default configuration file ([`60de019`](https://github.com/irtnog/lethbridge/commit/60de019291e2b227830e54dce88ac5e574c125a7))

* feat(cli): add copyright notice to version callback ([`ff4dc75`](https://github.com/irtnog/lethbridge/commit/ff4dc7513092e3b0b977323c98c61d2e4b709e00))

* feat(config): add an external configuration file ([`aef34aa`](https://github.com/irtnog/lethbridge/commit/aef34aafd9b5b1aaaa92e447d45b2f2a482a7edf))

* feat: configure logging ([`ef79107`](https://github.com/irtnog/lethbridge/commit/ef7910754f52f9ed406135ac0747bd9eb5469360))

* feat(database): set default values for selected columns ([`fce7810`](https://github.com/irtnog/lethbridge/commit/fce7810e3f6e758fcd972ff0a97027492301c785))

* feat(database): map the system&#39;s coordinates to separate x/y/z columns ([`ef52871`](https://github.com/irtnog/lethbridge/commit/ef52871012ff39c16bec5ab2e53af813061341e5))

* feat(database): begin defining the data model ([`d999300`](https://github.com/irtnog/lethbridge/commit/d999300a0602a129f1469077cf4c928c4aeeb92d))

* feat: initial commit ([`c9d17bd`](https://github.com/irtnog/lethbridge/commit/c9d17bd94b3592d5cd7909df153510c5dfba02ba))

### Refactor

* refactor(cli): switch to modern (Python 3.6+) annotated arguments ([`a902918`](https://github.com/irtnog/lethbridge/commit/a90291814d98fed4c5fd65ef3d761e3df8e509e6))

* refactor(config): pull defaults out into dedicated constants

This makes referring to (and testing against) the defaults easier. ([`3a5cd11`](https://github.com/irtnog/lethbridge/commit/3a5cd115d8643526c177615a0ea785dd3205d011))

* refactor: sort imports ([`318eb79`](https://github.com/irtnog/lethbridge/commit/318eb7934614b97ca7b99bdb0c9529409cb7708b))

* refactor(config): simplify configuration file handling

Configuration file creation, etc., is only necessary when actually
saving changed settings.  This will be driven by the user interface.

If the configuration file doesn&#39;t exist, silently skip it.  Only throw
an error at load time if the file exists but cannot be read for
whatever reason, on the assumption that if the configuration file
exists, it is supposed to be readable. ([`1a1b96b`](https://github.com/irtnog/lethbridge/commit/1a1b96bae7fea4f86e7ccd840b1da86d56319d4c))

* refactor(cli): use typer.secho for all application-level (not library) user comms ([`3aeba07`](https://github.com/irtnog/lethbridge/commit/3aeba07060bbbb1a19ec58634c6916a5a61061b6))

* refactor(lethbridge): initialize logging at CLI start time

This lets other tools use Lethbridge as a library and control things
like logging themselves. ([`808a85b`](https://github.com/irtnog/lethbridge/commit/808a85b05fc555796dc659ef0615cc6b8b4c18fc))

* refactor(cli): rename variables to make their puposes clearer ([`a37427d`](https://github.com/irtnog/lethbridge/commit/a37427d493b97ceb944a6a6d59554c1f1c62be1f))

* refactor(cli): modularize now to support subcommands later ([`a8628e5`](https://github.com/irtnog/lethbridge/commit/a8628e53c30774b0503e77d20acbd62f78c6a6cc))

* refactor(cli): add missing list item separator ([`02446ce`](https://github.com/irtnog/lethbridge/commit/02446ce87b181d28a68712c8f0966674c5c575cf))

* refactor(__main__): switch to relative imports ([`7735fb4`](https://github.com/irtnog/lethbridge/commit/7735fb4bf611b572373890ca444aee2baa4b1d74))

* refactor(__init__): determine app name at runtime based on package name ([`bbcaf30`](https://github.com/irtnog/lethbridge/commit/bbcaf30a35fd242412bad91af15df62131fec871))

* refactor(database): remove extraneous abstract class definition ([`ef4af5b`](https://github.com/irtnog/lethbridge/commit/ef4af5b0aeb0df9ef2406bbfb2f7aae263dbb4cf))

### Test

* test: install code coverage reporting plugin ([`ecf839b`](https://github.com/irtnog/lethbridge/commit/ecf839bdc8f28d3aaf35bbb39cb40e33656d57b7))

* test(database): convert engine test fixtures to database URIs

The planned interface expects URIs, not already running engines. ([`2abdf44`](https://github.com/irtnog/lethbridge/commit/2abdf44a1e7591782ed11fba1ad9cc7726ce87a6))

* test(database): install and test a cffi variant of psycopg2 ([`5387e50`](https://github.com/irtnog/lethbridge/commit/5387e50981b3b0f7afad7fd4b0fb38889b195d46))

* test(database): add a PostgreSQL database test fixture

This enables database module testing against both PostgreSQL and
SQLite databases.  The container build stage installs PostgreSQL and
performs the Python package install and test processes as an
unprivileged user, which are all required by pytest-postgresql. ([`37eb313`](https://github.com/irtnog/lethbridge/commit/37eb31384670326d58480b8e114ce261842d40b1))

* test(database): parametrize the database engine ([`0ca0f32`](https://github.com/irtnog/lethbridge/commit/0ca0f32be1e9007e4b97b96212266565987f1699))

* test: break down and sort imports ([`86a1aa9`](https://github.com/irtnog/lethbridge/commit/86a1aa9ab14e5beda639ec53206c59dcd306817a))

* test(cli): pair test filename with the corresponding module ([`0d4bfe5`](https://github.com/irtnog/lethbridge/commit/0d4bfe5caf30f2b8b1ead8a4e7088386933b2623))
