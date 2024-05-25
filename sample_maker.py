import random



if __name__=="__main__":
  input_filename="sample_input.txt"
  init_time=1715744138010
  types_of_log=[
    "RESOURCE_UNAVBL",
    "INTERNAL_SERVER_ERROR",
    "BAD_REQUEST",
    "BAD_GATEWAY",
    "PAGE_NOT_FOUND"
  ]
  num_logs=100
  cur_time=init_time
  with  open(input_filename,"w") as f:
    for i in range(num_logs):
      r_val=random.randint(1,4)
      if r_val==1:
        print(r_val,f"{cur_time};{random.choice(types_of_log)};{1e6*random.random()}",file=f)
        cur_time+=random.randint(1,10)
      elif r_val==2:
        print(r_val,f"{random.choice(types_of_log)}",file=f)
      elif r_val==3:
        term="BEFORE"
        if random.randint(0,1)==1:
          term="AFTER"
        print(r_val,f"{term} {random.randint(init_time,cur_time)}",file=f)
      elif r_val==4:
        term="BEFORE"
        if random.randint(0,1)==1:
          term="AFTER"
        print(r_val,f"{term} {random.choice(types_of_log)} {random.randint(init_time,cur_time)}",file=f)