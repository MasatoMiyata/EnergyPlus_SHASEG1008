## Run and postprocess IDF files for ASHRAE Standard 140
## 2021-03-25 E.Ono

#####################################
# Load libraries
#####################################
# load the packages
library(eplusr)
library(ggplot2)
library(reshape)

# install here package if not exists
if (!require("here", quietly = TRUE)) install.packages("here")

# turn off verbose information of eplusr package
eplusr_option(verbose_info = FALSE)

eplusr_option(autocomplete = TRUE)

# see what EnergyPlus has been installed
avail_eplus()

# use the example file from latest EnergyPlus installed
ver <- max(avail_eplus())

# parse IDD
#idd <- use_idd(ver, download = "auto")


run_EnergyPlus <- function (path_wd,path_idf,path_epw,case_name){

  idf <- read_idf(path = path_idf, idd = NULL)

  #tmp <- idf$Building
  #dt <- data.table::rbindlist(c(list(tmp$to_table()), lapply(tmp$ref_to_object(), function (x) x$to_table())))
  #dt[6,6] <- "FullInteriorAndExterior"
  #idf$update(dt)

  #tmp <- idf$"FenestrationSurface:Detailed"[["Block1:Zone1_Wall_S_Win_1"]]
  #dt <- data.table::rbindlist(c(list(tmp$to_table()), lapply(tmp$ref_to_object(), function (x) x$to_table())))
  #dt[3,6] <- 1002
  #idf$update(dt)

  #tmp <- idf$"FenestrationSurface:Detailed"[["Block1:Zone1_Wall_S_Win_2"]]
  #dt <- data.table::rbindlist(c(list(tmp$to_table()), lapply(tmp$ref_to_object(), function (x) x$to_table())))
  #dt[3,6] <- 1002
  #idf$update(dt)

  #idf$save(path_idf,"overwrite" = TRUE)


  #####################################
  # Run simulations
  #####################################

  job <- idf$run(path_epw, wait = TRUE)
  job <- idf$last_job()
  stopifnot(!is.null(job))

  key_values <- job$report_data_dict()$key_value
  names <- job$report_data_dict()$name
  N <- length(names)

  window_area <- 12 # floor area of seminar room from E+

  ta <- unlist(job$report_data("BLOCK1:ZONE1" ,"Zone Mean Air Temperature")[,6])
  qh <- unlist(job$report_data("BLOCK1:ZONE1" ,"Zone Air System Sensible Heating Rate")[,6])
  qc <- unlist(job$report_data("BLOCK1:ZONE1" ,"Zone Air System Sensible Cooling Rate")[,6])
  ri <- unlist(job$report_data("BLOCK1:ZONE1" ,"Zone Windows Total Transmitted Solar Radiation Rate")[,6])
  rh <- unlist(job$report_data("BLOCK1:ZONE1_ROOF" ,"Surface Outside Face Incident Solar Radiation Rate per Area")[,6])
  rn <- unlist(job$report_data("BLOCK1:ZONE1_WALL_N" ,"Surface Outside Face Incident Solar Radiation Rate per Area")[,6])
  re <- unlist(job$report_data("BLOCK1:ZONE1_WALL_E" ,"Surface Outside Face Incident Solar Radiation Rate per Area")[,6])
  rs <- unlist(job$report_data("BLOCK1:ZONE1_WALL_S" ,"Surface Outside Face Incident Solar Radiation Rate per Area")[,6])
  rw <- unlist(job$report_data("BLOCK1:ZONE1_WALL_W" ,"Surface Outside Face Incident Solar Radiation Rate per Area")[,6])

  # annual heating/cooling load
  qh_sum <- sum(qh)/1000/1000
  qc_sum <- sum(qc)/1000/1000

  # peak heating/cooling load
  qh_peak <- max(qh)/1000
  qc_peak <- max(qc)/1000

  # free-float temperature
  ta_max <- max(ta)
  ta_min <- min(ta)
  ta_ave <- mean(ta)

  # annual incident total
  rn_sum <- sum(rn)/1000
  re_sum <- sum(re)/1000
  rw_sum <- sum(rw)/1000
  rs_sum <- sum(rs)/1000
  rh_sum <- sum(rh)/1000
  ri_sum <- sum(ri)/window_area/1000

  # hourly solar incident
  date0 <- "2021-01-01"
  date1 <- "2021-03-05"
  Nday <- as.integer(difftime(date1,date0,units="days"))
  inds <- Nday*24 + 1
  inde <- Nday*24 + 24
  rs0305 <- rs[inds:inde]
  rw0305 <- rw[inds:inde]

  date1 <- "2021-07-27"
  Nday <- as.integer(difftime(date1,date0,units="days"))
  inds <- Nday*24 + 1
  inde <- Nday*24 + 24
  rs0727 <- rs[inds:inde]
  rw0727 <- rw[inds:inde]

  # hourly heating/cooling load
  date1 <- "2021-01-04"
  Nday <- as.integer(difftime(date1,date0,units="days"))
  inds <- Nday*24 + 1
  inde <- Nday*24 + 24
  q0104 <- (qh[inds:inde] - qc[inds:inde])/1000
  ta0104 <- ta[inds:inde]

  tmp <- c(qh_sum,qc_sum,qh_peak,qc_peak,rn_sum,re_sum,rw_sum,rs_sum,rh_sum,ri_sum,ta_max,ta_min,ta_ave,numeric(11))

  output <- data.frame(sum_peak=tmp,rs0305=rs0305,rw0305=rw0305,rs0727=rs0727,rw0727=rw0727,q0104=q0104,ta0104=ta0104)

  fname <- paste0(path_wd,"Case",case_name,"_postprocessed.csv")
  write.csv(as.matrix(output),fname)

}

path_wd <- "/Users/eikichiono/Documents/04_Association/SHASE/ECP/EnergyPlus_SHASEG1008/EnergyPlus_SHASEG1008/DesignBuilder/"
your_tool <- "EnergyPlus-o"
case_name <- "900-J2"
path_epw <- paste0(path_wd,"DRYCOLDTMY.epw")
path_idf <- paste0(path_wd,"Case",case_name,".idf")

run_EnergyPlus(path_wd,path_idf,path_epw,case_name)

#####################################
# Compare results
#####################################

load(paste0(path_wd,"trial_data.Rdata"))

# case_name <- "900"
tmp <- read.csv(paste0(path_wd,"Case",case_name,"_postprocessed.csv"))
qh_sum <- tmp[1,2]
qc_sum <- tmp[2,2]
qh_peak <- tmp[3,2]
qc_peak <- tmp[4,2]

color_table <- c(rep("darkgray",11),"cornflowerblue","salmon")

if (length(grep("FF",case_name)) == 0){
  A <- data.frame(tool=c(colnames(Aqh_sum),your_tool),"Annual_heating.MWh"=c(unlist(Aqh_sum[case_name,]),qh_sum))
  A["Annual_cooling.MWh"] <- c(unlist(Aqc_sum[case_name,]),qc_sum)
  A["Peak_heating.kW"] <- c(unlist(Aqh_peak[case_name,]),qh_peak)
  A["Peak_cooling.kW"] <- c(unlist(Aqc_peak[case_name,]),qc_peak)
  tmp <- melt(A, id="tool")
  
  p <- ggplot(tmp, aes(x=reorder(tool,seq(1,nrow(tmp))), y=value, fill=reorder(tool,seq(1,nrow(tmp))))) + 
    geom_col() + facet_wrap(~variable,nrow=1,ncol=(ncol(A)-1)) +
    labs(title=paste0("Case",case_name), x="Simulation tools" ,y="Heating/cooling load [MWh or kW]") + 
    theme(axis.text.x = element_text(angle = 90, hjust = 1))+ scale_fill_manual(values = color_table) +
    theme(legend.position = 'none')
  fname <- paste0(path_wd,"figures/Case",case_name,"_annual_peak_load.png")
  ggplot2::ggsave(fname,p, width=25, height=10, units = "cm", dpi=400)
}

if (length(grep("FF",case_name)) == 1 || case_name == "960"){
  A <- data.frame(tool=c(colnames(Aqh_sum),your_tool),Maximum_temperature=c(unlist(Ata_max[case_name,]),ta_max))
  A["Minimum_temperature"] <- c(unlist(Ata_min[case_name,]),ta_min)
  A["Average_temperature"] <- c(unlist(Ata_ave[case_name,]),ta_ave)
  tmp <- melt(A, id="tool")
  
  p <- ggplot(tmp, aes(x=reorder(tool,seq(1,nrow(tmp))), y=value, fill=reorder(tool,seq(1,nrow(tmp))))) + 
    geom_col() + facet_wrap(~variable,nrow=1,ncol=(ncol(A)-1)) +
    labs(title=paste0("Case",case_name), x="Simulation tools" ,y="Zone temperature [degC]") + 
    theme(axis.text.x = element_text(angle = 90, hjust = 1))+ scale_fill_manual(values = color_table) +
    theme(legend.position = 'none')
  fname <- paste0("./figures/Case",case_name,"_temperature_stat.png")
  ggplot2::ggsave(fname,p, width=40, height=10, units = "cm", dpi=400)
}

if (case_name == "600"){
  A <- data.frame(tool=c(colnames(Aqh_sum),your_tool),North=c(unlist(Ar_sum[1,]),rn_sum),
                  East=c(unlist(Ar_sum[2,]),re_sum),West=c(unlist(Ar_sum[3,]),rw_sum),
                  South=c(unlist(Ar_sum[4,]),rs_sum),Horizontal=c(unlist(Ar_sum[5,]),rh_sum))
  tmp <- melt(A, id="tool")

  Nvalue <- length(Ar_sum[1,is.finite(Ar_sum[1,])])
  color_table <- c(rep("darkgray",Nvalue),"salmon")
  
  p <- ggplot(tmp, aes(x=reorder(tool,seq(1,nrow(tmp))), y=value, fill=reorder(tool,seq(1,nrow(tmp))))) + 
    geom_col() + facet_wrap(~variable,nrow=1,ncol=(ncol(A)-1)) +
    labs(title=paste0("Case",case_name), x="Simulation tools" ,y="Annual incident total [kWh/m2]") + 
    theme(axis.text.x = element_text(angle = 90, hjust = 1))+ scale_fill_manual(values = color_table) +
    theme(legend.position = 'none')
  p
  fname <- paste0("./figures/Case",case_name,"_annual_incident.png")
  ggplot2::ggsave(fname,p, width=40, height=10, units = "cm", dpi=400)
}





#####################################
# Load trial results
#####################################

# library(readxl)
# 
# fname <- "/Users/eikichiono/Documents/04_Association/SHASE/ECP/EnergyPlus_SHASEG1008/EnergyPlus_SHASEG1008/results/SHASEG1008_EnergyPlus-miyata_結果まとめ.xls"
# results = read_excel(fname, sheet = 2)
# 
# tool_names <- unlist(results[14,2:13])
# case_numbers <- unlist(results[17:51,1])
# 
# Aqh_sum <- matrix(as.numeric(unlist(results[17:51,2:13])),nrow=length(case_numbers),ncol=length(tool_names))
# colnames(Aqh_sum) <- tool_names
# rownames(Aqh_sum) <- case_numbers
# 
# Aqc_sum <- matrix(as.numeric(unlist(results[57:91,2:13])),nrow=length(case_numbers),ncol=length(tool_names))
# colnames(Aqc_sum) <- tool_names
# rownames(Aqc_sum) <- case_numbers
# 
# Aqh_peak <- matrix(as.numeric(unlist(results[100:134,2:13])),nrow=length(case_numbers),ncol=length(tool_names))
# colnames(Aqh_peak) <- tool_names
# rownames(Aqh_peak) <- case_numbers
# 
# Aqc_peak <- matrix(as.numeric(unlist(results[145:179,2:13])),nrow=length(case_numbers),ncol=length(tool_names))
# colnames(Aqc_peak) <- tool_names
# rownames(Aqc_peak) <- case_numbers
# 
# case_name_J <- c("900-J1-1","900-J1-2","900-J2","900-J3")
# tmp <- matrix(as.numeric(unlist(results[188:191,2:5])),nrow=4,ncol=4)
# tmp <- cbind(matrix(numeric(4*8),nrow=4),tmp)
# colnames(tmp) <- tool_names
# rownames(tmp) <- case_name_J
# Aqh_sum <- rbind(Aqh_sum,tmp)
# 
# tmp <- matrix(as.numeric(unlist(results[188:191,8:11])),nrow=4,ncol=4)
# tmp <- cbind(matrix(numeric(4*8),nrow=4),tmp)
# colnames(tmp) <- tool_names
# rownames(tmp) <- case_name_J
# Aqc_sum <- rbind(Aqc_sum,tmp)
# 
# tmp <- matrix(as.numeric(unlist(results[197:200,2:5])),nrow=4,ncol=4)
# tmp <- cbind(matrix(numeric(4*8),nrow=4),tmp)
# colnames(tmp) <- tool_names
# rownames(tmp) <- case_name_J
# Aqh_peak <- rbind(Aqh_peak,tmp)
# 
# tmp <- matrix(as.numeric(unlist(results[197:200,8:11])),nrow=4,ncol=4)
# tmp <- cbind(matrix(numeric(4*8),nrow=4),tmp)
# colnames(tmp) <- tool_names
# rownames(tmp) <- case_name_J
# Aqc_peak <- rbind(Aqc_peak,tmp)
# 
# Ata_max <- matrix(as.numeric(unlist(results[225:229,2:13])),nrow=5,ncol=length(tool_names))
# colnames(Ata_max) <- tool_names
# rownames(Ata_max) <- unlist(results[225:229,1])
# 
# Ata_min <- matrix(as.numeric(unlist(results[234:238,2:13])),nrow=5,ncol=length(tool_names))
# colnames(Ata_min) <- tool_names
# rownames(Ata_min) <- unlist(results[225:229,1])
# 
# Ata_ave <- matrix(as.numeric(unlist(results[243:247,2:13])),nrow=5,ncol=length(tool_names))
# colnames(Ata_ave) <- tool_names
# rownames(Ata_ave) <- unlist(results[225:229,1])
# 
# Ar_sum <- matrix(as.numeric(unlist(results[265:269,2:13])),nrow=5,ncol=length(tool_names))
# colnames(Ar_sum) <- tool_names
# rownames(Ar_sum) <- unlist(results[265:269,1])
# 
# Ari_sum <- matrix(as.numeric(unlist(rbind(results[284:285,2:13],results[304:305,2:13]))),nrow=4,ncol=length(tool_names))
# colnames(Ari_sum) <- tool_names
# rownames(Ari_sum) <- c(unlist(results[284:285,1]),unlist(results[304:305,1]))
# 
# Ars0305 <- matrix(as.numeric(unlist(results[320:343,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Ars0305) <- tool_names
# rownames(Ars0305) <- 1:24
# 
# Arw0305 <- matrix(as.numeric(unlist(results[360:383,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Arw0305) <- tool_names
# rownames(Arw0305) <- 1:24
# 
# Ars0727 <- matrix(as.numeric(unlist(results[400:423,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Ars0727) <- tool_names
# rownames(Ars0727) <- 1:24
# 
# Arw0727 <- matrix(as.numeric(unlist(results[440:463,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Arw0727) <- tool_names
# rownames(Arw0727) <- 1:24
# 
# Ata0104_600FF <- matrix(as.numeric(unlist(results[479:502,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Ata0104_600FF) <- tool_names
# rownames(Ata0104_600FF) <- 1:24
# 
# Ata0104_900FF <- matrix(as.numeric(unlist(results[519:542,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Ata0104_900FF) <- tool_names
# rownames(Ata0104_900FF) <- 1:24
# 
# Ata0727_650FF <- matrix(as.numeric(unlist(results[559:582,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Ata0727_650FF) <- tool_names
# rownames(Ata0727_650FF) <- 1:24
# 
# Ata0727_950FF <- matrix(as.numeric(unlist(results[599:622,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Ata0727_950FF) <- tool_names
# rownames(Ata0727_950FF) <- 1:24
# 
# Aq0104_600 <- matrix(as.numeric(unlist(results[639:662,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Aq0104_600) <- tool_names
# rownames(Aq0104_600) <- 1:24
# 
# Aq0104_900 <- matrix(as.numeric(unlist(results[679:702,2:13])),nrow=24,ncol=length(tool_names))
# colnames(Aq0104_900) <- tool_names
# rownames(Aq0104_900) <- 1:24
# 
# Atbin <- matrix(as.numeric(unlist(results[720:868,2:13])),nrow=149,ncol=length(tool_names))
# colnames(Atbin) <- tool_names
# rownames(Atbin) <- unlist(results[720:868,1])
# 
# save.image("trial_data.Rdata")


# library(openxlsx)
# results <- read.xlsx("Appendix C 熱負荷単室・複数室テスト用入力ファイル_DB.xlsx", sheet="計算結果入力シート")
# 
# tool_names <- results[8,2:12]
# case_numbers <- results[11:45,1]
# 
# Aqh_sum <- matrix(as.numeric(unlist(results[11:45,2:12])),nrow=length(case_numbers),ncol=length(tool_names))
# colnames(Aqh_sum) <- tool_names
# rownames(Aqh_sum) <- case_numbers
# 
# Aqc_sum <- matrix(as.numeric(unlist(results[51:85,2:12])),nrow=length(case_numbers),ncol=length(tool_names))
# colnames(Aqc_sum) <- tool_names
# rownames(Aqc_sum) <- case_numbers
# 
# Aqh_peak <- matrix(as.numeric(unlist(results[91:125,2:12])),nrow=length(case_numbers),ncol=length(tool_names))
# colnames(Aqh_peak) <- tool_names
# rownames(Aqh_peak) <- case_numbers
# 
# Aqc_peak <- matrix(as.numeric(unlist(results[131:165,2:12])),nrow=length(case_numbers),ncol=length(tool_names))
# colnames(Aqc_peak) <- tool_names
# rownames(Aqc_peak) <- case_numbers
# 
# case_name_J <- c("900-J1-1","900-J1-2","900-J2","900-J3")
# tmp <- matrix(as.numeric(unlist(results[171:174,2:4])),nrow=4,ncol=3)
# tmp <- cbind(matrix(numeric(4*8),nrow=4),tmp)
# colnames(tmp) <- tool_names
# rownames(tmp) <- case_name_J
# Aqh_sum <- rbind(Aqh_sum,tmp)
# 
# tmp <- matrix(as.numeric(unlist(results[171:174,8:10])),nrow=4,ncol=3)
# tmp <- cbind(matrix(numeric(4*8),nrow=4),tmp)
# colnames(tmp) <- tool_names
# rownames(tmp) <- case_name_J
# Aqc_sum <- rbind(Aqc_sum,tmp)
# 
# tmp <- matrix(as.numeric(unlist(results[179:182,2:4])),nrow=4,ncol=3)
# tmp <- cbind(matrix(numeric(4*8),nrow=4),tmp)
# colnames(tmp) <- tool_names
# rownames(tmp) <- case_name_J
# Aqh_peak <- rbind(Aqh_peak,tmp)
# 
# tmp <- matrix(as.numeric(unlist(results[179:182,8:10])),nrow=4,ncol=3)
# tmp <- cbind(matrix(numeric(4*8),nrow=4),tmp)
# colnames(tmp) <- tool_names
# rownames(tmp) <- case_name_J
# Aqc_peak <- rbind(Aqc_peak,tmp)
# 
# Ata_max <- matrix(as.numeric(unlist(results[202:206,2:12])),nrow=5,ncol=length(tool_names))
# colnames(Ata_max) <- tool_names
# rownames(Ata_max) <- results[202:206,1]
# 
# Ata_min <- matrix(as.numeric(unlist(results[211:215,2:12])),nrow=5,ncol=length(tool_names))
# colnames(Ata_min) <- tool_names
# rownames(Ata_min) <- results[202:206,1]
# 
# Ata_ave <- matrix(as.numeric(unlist(results[220:224,2:12])),nrow=5,ncol=length(tool_names))
# colnames(Ata_ave) <- tool_names
# rownames(Ata_ave) <- results[202:206,1]
# 
# Ar_sum <- matrix(as.numeric(unlist(results[234:238,2:12])),nrow=5,ncol=length(tool_names))
# colnames(Ar_sum) <- tool_names
# rownames(Ar_sum) <- results[234:238,1]
# 
# Ari_sum <- matrix(as.numeric(unlist(rbind(results[252:253,2:12],results[262:263,2:12]))),nrow=4,ncol=length(tool_names))
# colnames(Ari_sum) <- tool_names
# rownames(Ari_sum) <- c(results[252:253,1],results[262:263,1])
# 
# Ars0305 <- matrix(as.numeric(unlist(results[275:298,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Ars0305) <- tool_names
# rownames(Ars0305) <- 1:24
# 
# Arw0305 <- matrix(as.numeric(unlist(results[308:331,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Arw0305) <- tool_names
# rownames(Arw0305) <- 1:24
# 
# Ars0727 <- matrix(as.numeric(unlist(results[341:364,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Ars0727) <- tool_names
# rownames(Ars0727) <- 1:24
# 
# Arw0727 <- matrix(as.numeric(unlist(results[374:397,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Arw0727) <- tool_names
# rownames(Arw0727) <- 1:24
# 
# Ata0104_600FF <- matrix(as.numeric(unlist(results[406:429,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Ata0104_600FF) <- tool_names
# rownames(Ata0104_600FF) <- 1:24
# 
# Ata0104_900FF <- matrix(as.numeric(unlist(results[438:461,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Ata0104_900FF) <- tool_names
# rownames(Ata0104_900FF) <- 1:24
# 
# Ata0727_650FF <- matrix(as.numeric(unlist(results[469:492,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Ata0727_650FF) <- tool_names
# rownames(Ata0727_650FF) <- 1:24
# 
# Ata0727_950FF <- matrix(as.numeric(unlist(results[501:524,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Ata0727_950FF) <- tool_names
# rownames(Ata0727_950FF) <- 1:24
# 
# Aq0104_600 <- matrix(as.numeric(unlist(results[534:557,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Aq0104_600) <- tool_names
# rownames(Aq0104_600) <- 1:24
# 
# Aq0104_900 <- matrix(as.numeric(unlist(results[567:590,2:12])),nrow=24,ncol=length(tool_names))
# colnames(Aq0104_900) <- tool_names
# rownames(Aq0104_900) <- 1:24
# 
# Atbin <- matrix(as.numeric(unlist(results[600:748,2:12])),nrow=149,ncol=length(tool_names))
# colnames(Atbin) <- tool_names
# rownames(Atbin) <- results[600:748,1]
# 
# save.image("trial_data.Rdata")



