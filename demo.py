from student.pipline.pipeline import Pipeline
from student.configuration import Configuartion
from student.constants import get_current_time_stamp



obj=Pipeline(config=Configuartion(current_time_stamp=get_current_time_stamp()))
obj.run_pipeline()