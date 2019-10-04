from parsl.data_provider.http import _http_stage_in_app
from parsl.data_provider.staging import Staging
from parsl.data_provider.files import File
from parsl.config import Config
import parsl
import time
class CachingHTTPStaging(Staging):

    def __init__(self):    
        super().__init__()
        self.so_far = {}  # type: Dict[str, Future]

    def can_stage_in(self, file):
        print("CHECKING CAN_STAGE_IN")
        return file.scheme == "http"

    def stage_in(self, dm: "DataManager", executor: str, file: File, parent_fut):
        """ http://host/my/file ==> /http/host/my/this """

        print("CACHING HTTP STAGE IN")
        working_dir = dm.dfk.executors[executor].working_dir

        if working_dir:
            file.local_path = os.path.join(working_dir, file.filename)
        else:
            file.local_path = file.filename

        if file.url in self.so_far:   # already in cache case
            print("CACHE PATH")
            return self.so_far[file.url]
        else: # not in cache
 
            print("NOT CACHE PATH")
            stage_in_app = _http_stage_in_app(dm, executor=executor)
            app_fut = stage_in_app(working_dir, outputs=[file], staging_inhibit_output=True, parent_fut=parent_fut)
            self.so_far[file.url] = app_fut
            return app_fut._outputs[0]

@parsl.python_app
def my_app(myfile):
    print("in my_app")

parsl.load(Config(executors=[parsl.ThreadPoolExecutor(storage_access=[CachingHTTPStaging()])]))

infile = File("http://www.hawaga.org.uk/index.html")

r = my_app(infile)
r.result()

print("done with r")
time.sleep(3)

s = my_app(infile)
s.result()
print("done with s")

