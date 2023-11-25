class Solution:

    @staticmethod
    def isInterleave( s1: str, s2: str, s3: str) -> bool:
        
        dp=[-1]*(len(s2)+1)
        
    
        if (len(s1)+len(s2))!=len(s3):
            return False

        if s1=="" or s2=="":
            if s2==s3 or s1==s3:
                return True
            else:
                return False
        

        if s1[0]==s3[0] or s2[0]==s3[0]:
            dp[0]=0
        else:
            return False
        m=-1
        for i in range(len(s1)+1):
            #print(s1[i])
            for j in range(len(dp)):      

                if dp[j]!=-1 and i!=0:

                    if s1[i-1]==s3[ dp[j] ]:
                        #print("yes")
                        if (i<len(s1) and s1[i]==s3[ dp[j]+1]) or (j<len(s2) and s2[j]==s3[ dp[j]+1]):
                            dp[j]+=1
                        else:
                            dp[j]=-1
                    else:
                        dp[j]=-1
                
                elif j!=0:

                    if dp[j-1]!=-1 and s2[j-1]==s3[ dp[j-1] ]:
                        if (j<len(s2) and s2[j]==s3[ dp[j-1]+1 ]) or (i<len(s1) and s1[i]==s3[ dp[j-1] +1 ]):
                            dp[j]=dp[j-1]+1
                        else:
                            dp[j]=-1
                    else:
                        dp[j]=-1
                
                if m<dp[j]:
                    m=dp[j]
            print(dp)
        
    
        if m+1==len(s3):
            return True
        else:
            return False
        
def is_interwoven(s: str, x: str, y: str) -> bool:
    
    dp = [[False for _ in range(len(y)+1)] for _ in range(len(x) + 1)]
    
    if len(x) + len(y) != len(s):
        return False
    for i in range(len(x)+1):
        for j in range(len(y)+1):
            if i == 0 and j == 0:
                dp[i][j] = True
            elif j == 0:
                dp[i][j] = dp[i - 1][j] and x[i - 1] == s[i + j - 1]
            else:
                dp[i][j] = ((dp[i - 1][j] and x[i - 1] == s[i + j - 1]) or
                               (dp[i][j - 1] and y[j - 1] == s[i + j - 1]))
                
    print(dp)
    return dp[len(x)][len(y)]

if __name__ == '__main__':
    str1 = "101"
    str2 = "010"
    str3 = "011010"
    #print(Solution.isInterleave(str1, str2, str3))
    print(is_interwoven(str3, str1, str2))