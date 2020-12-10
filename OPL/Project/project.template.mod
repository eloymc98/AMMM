 int nLocations = ...;
 int nCities = ...;
 int nTypes = ...;
		   
 range L = 1..nLocations;
 range C = 1..nCities;
 range T = 1..nTypes;

 int posCities[C][1..2] = ...;
 int posLocations[L][1..2] = ...;
 int p[C] = ...;

 float d_city[T] = ...;
 int cap [T] = ...;
 int cost [T] = ...;

 float d_center = ...;
 
 int distance_l1l2[l1 in L][l2 in L];
 float distance_cl[c in C][l in L];

execute {
  var distance = 0;
  
  for(var i=1;i<=nLocations;i++){
    for(var j=i+1;j<=nLocations;j++){
    	distance=Math.sqrt(Math.pow(posLocations[i][1]-posLocations[j][1],2) + Math.pow(posLocations[i][2]-posLocations[j][2],2))
    	if(distance>=d_center){
    	  writeln( 'L1:' + i + ' L2:' + j)
    	  distance_l1l2[i][j] = 1;
    	}
    	else{
    	  distance_l1l2[i][j] = 0;
    	}
    }
  }
  
  for(var i=1;i<=nCities;i++){
    for(var j=1;j<=nLocations;j++){
    	distance_cl[i][j]=Math.sqrt(Math.pow(posCities[i][1]-posLocations[j][1],2) + Math.pow(posCities[i][2]-posLocations[j][2],2));
    }
  }
		
};
			  
// Define your decision variables and any other auxiliary data here.
// You can run an execute block if needed.
dvar boolean located[l in L, t in T];
dvar boolean primary[c in C, l in L];
dvar boolean secondary[c in C, l in L];



 minimize // ... Write the objective function.
 sum(l in L, t in T) located[l,t]*cost[t];
 subject to {

  // Each city is served by one primary center
	forall(c in C)
	sum(l in L)  primary[c,l] == 1;

  // Each city is served by one secondary center
	forall(c in C)
	sum(l in L) secondary[c,l] == 1;

  // (igual sobra) Primary center and secondary center of a city must be different
	forall(c in C, l in L)
	  primary[c,l] + secondary[c,l] <= 1;
	
  // A location can only have one center
  	forall(l in L) 
  	sum(t in T) located[l,t] <= 1;
  	
  // If a location serves a city as primary or secondary center,
  // it must have a center
	forall(c in C, l in L)
	  sum(t in T) located[l,t] >= primary[c,l] + secondary[c,l];
	  
  // Capacity limitations
  	forall(l in L, t in T)
  	  sum(c in C) (primary[c,l] + 0.1*secondary[c,l])*p[c] <= cap[t] + sum(c in C) p[c]*(1-located[l,t]);
  	  
  // Distance between centers
  	forall(l1 in L, l2 in L : l1<l2 && distance_l1l2[l1,l2]==0)
  	  sum(t in T) (located[l1,t] + located[l2,t]) <= 1;
	
  // Working distance of primary centers
  	forall(c in C, l in L, t in T: distance_cl[c][l] > d_city[t])
 		located[l][t] + primary[c][l] <=1;
 
   // Working distance of secondary centers
  	forall(c in C, l in L, t in T: distance_cl[c][l] > 3 * d_city[t])
 		located[l][t] + secondary[c][l] <=1;
 }

// You can run an execute block if needed.

execute{
  var population = 0;

  
  for(var i=1; i<=nLocations; i++){
    for(var j=1; j<=nTypes; j++){
       if(located[i][j]==1){
         population = 0
         for(var k=1; k<=nCities; k++){
           if(primary[k][i]==1){
             population+=p[k]
           }
           if(secondary[k][i]==1){
             population+=0.1*p[k]
           }
          
         }
          writeln('Location ' + i + ' has a center of type '+ j +'. It serves ' + population + ' inhabitants, max is '+ cap[j])
        
  		}
    }
  }
  
  for(var c=1; c<=nCities; c++){
    for(var l=1; l<=nLocations; l++){
      for(var t=1; t<=nTypes; t++){
        if(primary[c][l]==1 && located[l][t]==1){
        	writeln('City ' + c + ' primary center is at location ' + l + ' (distance ' + distance_cl[c][l] + ', max is ' + d_city[t] + ')')
      	}
      	if(secondary[c][l]==1 && located[l][t]==1){
        	writeln('City ' + c + ' secondary center is at location ' + l + ' (distance ' + distance_cl[c][l] + ', max is ' + 3*d_city[t] + ')')
      	}
      }
      
    }
  }    
  
 
}
