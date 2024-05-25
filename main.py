from collections import defaultdict
import sys

class QueryTuple:
  def __init__(self,x,y,z):
    self.x=x
    self.y=y
    self.z=z
  
  def combine(self,other):
    return QueryTuple(
      min(self.x,other.x)
      ,max(self.y,other.y)
      ,self.z+other.z
      )
  
  @classmethod
  def getDefault(cls):
    return QueryTuple(0.0,0.0,0.0)
  
  def __str__(self):
    
    return f"Min: {self.x}, Max: {self.y}, Mean: {self.z}"


class QueryHandler:
  """
    The mean part is stored as the sum but when queried, gets returned as the mean
  """
  def __init__(self):
    self.bitwiseArrays=[
      []
    ]
    self.timeStamps=[]
    self.globalAns=None
  
  def getWholeRange(self):
    if not self.globalAns:
      return QueryTuple.getDefault()
    
    ans=QueryTuple.getDefault()
    ans.x=self.globalAns.x
    ans.y=self.globalAns.y
    ans.z=self.globalAns.z/len(self.timeStamps)

    return ans

  def addEntry(self,t:int,elem:float):
    self.timeStamps.append(t)
    self.bitwiseArrays[0].append(QueryTuple(elem,elem,elem))

    if not self.globalAns:
      self.globalAns=self.bitwiseArrays[0][-1]
    else:
      self.globalAns=QueryTuple.combine(
        self.globalAns
        ,self.bitwiseArrays[0][-1]
      )

    while len(self.bitwiseArrays[0])>=(1<<len(self.bitwiseArrays)):
      self.bitwiseArrays.append([])
    
    fresh_index=len(self.bitwiseArrays[0])-1
    for k in range(1,len(self.bitwiseArrays)):
      new_len=(1<<(k-1))
      new_val=QueryTuple.combine(
        self.bitwiseArrays[k-1][fresh_index-new_len+1],
        self.bitwiseArrays[k-1][fresh_index-2*new_len+1]
      )
      self.bitwiseArrays[k].append(new_val)

  def __query_internal_range(self,a,b):
    if(a>b):
      return QueryTuple.getDefault()
    
    temp_len=b-a+1
    K_val=0
    while (1<<(K_val))<=temp_len:
      K_val+=1
    
    K_val-=1
    partialAns=QueryTuple.combine(
      self.bitwiseArrays[K_val][a],
      self.bitwiseArrays[K_val][b-(1<<K_val)+1]
    )

    ans_sum=0
    pointer=a
    for k in range(K_val,-1,-1):
      if pointer+(1<<k)-1<=b:
        ans_sum+=self.bitwiseArrays[k][pointer].z
        pointer+=(1<<k)
    
    partialAns.z=ans_sum/temp_len

    return partialAns
      
  def queryBefore(self,t:int):
    # find x such that self.timeStamps[x]<t
    # calculate lowerbound(t) and then go one step behind
    start=0
    end=len(self.timeStamps)
    if(end==0):
      return QueryTuple.getDefault()
    
    while start<end:
      mid=(start+end)//2
      if self.timeStamps[mid]<t:
        start=mid+1
      else:
        end=mid
    

    if start==0:
      return QueryTuple.getDefault()
    start-=1

    return self.__query_internal_range(0,start)
  
  def queryAfter(self,t:int):
    # find x such that self.timeStamps[x]>t
    # calculate upperbound(t)
    start=0
    end=len(self.timeStamps)
    if(end==0):
      return QueryTuple.getDefault()
    
    while start<end:
      mid=(start+end)//2
      if self.timeStamps[mid]<=t:
        start=mid+1
      else:
        end=mid
    
    if start==len(self.timeStamps):
      return QueryTuple.getDefault()
    
    return self.__query_internal_range(start,len(self.timeStamps)-1)
  



if __name__=="__main__":
  input_filename="input.txt"
  output_filename="output.txt"
  
  if len(sys.argv)>=3:
    input_filename=sys.argv[1]
    output_filename=sys.argv[2]

  queryList=[]
  with open(input_filename,'r') as f:
    queryList=list(map(lambda x:x.strip('\r\n').strip('\n'),f.readlines()))


  ansList=[]
  globalQueryHandler=QueryHandler()
  logWiseQueryHandler=defaultdict(QueryHandler)

  for query in queryList:
    partialSplit=query.split(' ',1)
    restInput=partialSplit[1].strip()
    typeInput=int(partialSplit[0])

    if typeInput==1:
      t,l,s=restInput.split(';')
      t=int(t)
      s=float(s)

      globalQueryHandler.addEntry(t,s)
      logWiseQueryHandler[l].addEntry(t,s)

      ansList.append("No output")

    elif typeInput==2:
      l=restInput

      ansList.append(str(logWiseQueryHandler[l].getWholeRange()))

    elif typeInput==3:
      timetype,t=restInput.split()
      t=int(t)
      if timetype.upper()=="BEFORE":
        ansList.append(str(globalQueryHandler.queryBefore(t)))
      elif timetype.upper()=="AFTER":
        ansList.append(str(globalQueryHandler.queryAfter(t)))
      else:
        raise Exception(f"Unsupported operation of type 3: {timetype}")
      
    elif typeInput==4:
      timetype,l,t=restInput.split()
      t=int(t)

      qObject=logWiseQueryHandler[l]

      if timetype.upper()=="BEFORE":
        ansList.append(str(qObject.queryBefore(t)))
      elif timetype.upper()=="AFTER":
        ansList.append(str(qObject.queryAfter(t)))
      else:
        raise Exception(f"Unsupported operation of type 4: {timetype}")
      

  with open(output_filename,'w') as f:
    for ans in ansList:
      f.write(ans+'\n')




















