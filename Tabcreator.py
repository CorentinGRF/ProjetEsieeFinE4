tab = np.zeros((rows,columns))
nbr_geese = len(geese)
            
for i range(nbr_geese): for j in range(len(geese[i])): tab[row_col(geese[i][j], columns) ] = j*nbr_geese

for pos in food: tab[row_col(pos, columns) ] = -1
        
tab2 = tab/4
tab3 = tab%4
#n/len(nbr_geese)
#n%len(nbr_geese)
