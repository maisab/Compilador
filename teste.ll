; ModuleID = "programaModulo"
target datalayout = ""

declare float @"printf_f"(float %".1") 

declare float @"scanf_f"() 

@"global.g" = external    global i32
@"global.h" = external    global float
define void @"main"() 
{
entry:
  %".2" = call float (float) @"printf_f"(float 0x4000000000000000)
}
