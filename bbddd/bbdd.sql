create schema maratongaby;


use maratongaby;

show tables;

create table entrada
(
    idEntrada     int         not null primary key auto_increment,
    idCategoria   int         not null,
    idTipoCarrera int         not null,
    idFactura     int         not null,
    precioEntrada float(5, 2) not null
);



create table factura
(
    idFactura int not null primary key auto_increment,
    idCliente int not null
);

create table cliente
(
    idCliente       int         not null primary key auto_increment,
    nameCliente     varchar(50) not null,
    apellidoCliente varchar(50) not null,
    cedulaCliente   int         not null
);

create table categoria
(
    idCategoria     int          not null primary key auto_increment,
    nameCategoria   varchar(100) not null,
    precioCategoria float(5, 2)  not null
);


create table tipoCarrera
(
    idTipoCarrera     int          not null primary key auto_increment,
    nameTipoCarrera   varchar(100) not null,
    precioTipoCarrera float(5, 2)  not null
);


alter table factura
    add constraint fk_idClienteFactura foreign key (idCliente) references cliente (idCliente);
alter table entrada
    add constraint fk_idENtradaCategoria foreign key (idCategoria) references categoria (idCategoria);
alter table entrada
    add constraint fk_idEntradaTipoCarrera foreign key (idTipoCarrera) references tipoCarrera (idTipoCarrera);
alter table entrada
    add constraint fk_idEntradaFactura foreign key (idFactura) references factura (idFactura);
alter table entrada
    add column fechaHora timestamp default current_timestamp;

insert into categoria (nameCategoria, precioCategoria)
values ("Normal", 120.12),
       ("Senior", 150.25),
       ("Discapacitados", 100),
       ("Tercera Edad", 152);


insert into tipoCarrera (nameTipoCarrera, precioTipoCarrera)
values ("5k", 20),
       ("10k", 25),
       ("22k", 50);



select *
from cliente;
select *
from factura;
select *
from categoria;
select *
from tipoCarrera;
select *
from entrada;

create view datosEntradasfactura as
select e.idEntrada,
       e.idFactura,
       c.nameCategoria,
       tC.nameTipoCarrera,
       e.precioEntrada,
       date_format(e.fechaHora, "%d/%m/%Y") as Fecha
from entrada e

         inner join categoria c on e.idCategoria = c.idCategoria
         inner join tipoCarrera tC on e.idTipoCarrera = tC.idTipoCarrera;

show tables;

select *
from factura;


select *
from factura;


alter table factura
    add column status int not null default 0;
show tables;


create table status
(
    idStatus   int not null primary key,
    nameStatus varchar(50)
);


insert into status (idStatus, nameStatus)
values (0, "Abierto"),
       (1, "Cerrado");

alter table factura
    add constraint fk_idstatusFactura foreign key (status) references status (idStatus);


select *
from status;
select *
from factura
         inner join status s on factura.status = s.idStatus;

select * from factura;

update factura set status=0 where idFactura= 3;


alter table factura add column precioTotal float(5,2) not null default 0;
alter table factura add column fechaCreacion timestamp default current_timestamp;

select * from factura;
create view datoslistafacturas as
select f.idFactura,
       concat(c.nameCliente, ' ', c.apellidoCliente) as NombreCompleto,
       s.nameStatus,
       f.precioTotal,
       date_format(f.fechaCreacion, "%d/%m/%Y") as Fecha

from factura f
         inner join cliente c on f.idCliente = c.idCliente
        inner join status s on f.status = s.idStatus

;
select * from datoslistafacturas order by idFactura;