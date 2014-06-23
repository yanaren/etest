DELIMITER ;;

use tcheck_db;;

DROP PROCEDURE if exists update_vs_available;
CREATE PROCEDURE update_vs_available(
in vs_addr char(255) character set gbk,
in avail int
)
begin

  update vs set available = avail where address =  vs_addr;

end;;

DELIMITER ;