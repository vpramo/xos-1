
# Copyright 2017-present Open Networking Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from basetest import BaseToscaTest

from core.models import Service

class EngineTest(BaseToscaTest):
    tests = ["intrinsic_get_artifact",
             "intrinsic_get_script_env",
             "intrinsic_get_script_env_noisy" ]

    def cleanup(self):
        self.try_to_delete(Service, name="testservice")

    def intrinsic_get_artifact(self):
        self.assert_noobj(Service, "testservice")
        file("/tmp/somevar","w").write("somevalue")
        self.execute(self.make_nodetemplate("testservice", "tosca.nodes.Service",
                                            props={"public_key": "{ get_artifact: [ SELF, somevar, LOCAL_FILE] }"},
                                            artifacts={"somevar": "/tmp/somevar"}))
        self.assert_obj(Service, "testservice", public_key="somevalue")

    def intrinsic_get_script_env(self):
        self.assert_noobj(Service, "testservice")
        file("/tmp/somescript","w").write( \
"""#! /bin/bash
FOO=123
BAR=456
JUNK=789
""")
        self.execute(self.make_nodetemplate("testservice", "tosca.nodes.Service",
                                            props={"public_key": "{ get_script_env: [ SELF, somescript, BAR, LOCAL_FILE] }"},
                                            artifacts={"somescript": "/tmp/somescript"}))
        self.assert_obj(Service, "testservice", public_key="456")

    def intrinsic_get_script_env_noisy(self):
        self.assert_noobj(Service, "testservice")
        file("/tmp/somescript","w").write( \
"""#! /bin/bash
echo "junk"
echo "oh no! something got written to stderr! This always breaks stuff!" >&2
FOO=123
echo "more junk"
BAR=456
echo "even more junk"
JUNK=789
echo "BAR=oops"
""")
        self.execute(self.make_nodetemplate("testservice", "tosca.nodes.Service",
                                            props={"public_key": "{ get_script_env: [ SELF, somescript, BAR, LOCAL_FILE] }"},
                                            artifacts={"somescript": "/tmp/somescript"}))
        self.assert_obj(Service, "testservice", public_key="456")

if __name__ == "__main__":
    EngineTest()
